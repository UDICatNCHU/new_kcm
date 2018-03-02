#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymongo, os, math, json_lines, psutil, logging, sys
import gridfs
import multiprocessing as mp
from pymongo import MongoClient
from ngram import NGram
from kcm.utils.clean_and_segmented_sentences import clean_and_segmented_sentences
from kcm.utils.graceful_auto_reconnect import graceful_auto_reconnect
from kcm.utils.deep_getsizeof import deep_getsizeof
from collections import defaultdict
from itertools import combinations
logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='buildKCM.log', level=logging.INFO)


class KCM(object):
    def __init__(self, input_dir, lang='zh_TW', uri=None):

        self.lang = lang
        self.input_dir = input_dir
        self.uri = uri
        self.db = MongoClient(self.uri).nlp
        self.Collect = self.db['kcm_{}'.format(self.lang)]
        self.KCMCollect = self.db['kcm_real']
        self.fs = gridfs.GridFS(self.db) 
        self.cpus = mp.cpu_count()
        # ngram search
        # self.kcmNgram = NGram((i['key'] for i in self.KCMCollect.find({}, {'key':1, '_id':False})))

    def build(self):
        @graceful_auto_reconnect
        def cut_cal_and_insert(filepaths):
            Collect = MongoClient(self.uri).nlp['kcm_{}'.format(self.lang)]

            for index, filepath in enumerate(filepaths):
                if index%10 == 0:
                    logging.info("已處理 %d 個檔案" % index)
                table = defaultdict(dict)

                with open(filepath, 'r') as f:
                    for article in json_lines.reader(f):
                        sentences = clean_and_segmented_sentences(self.lang, article)
                        for sentence in sentences:
                            for word1, word2 in combinations(sentence, 2):
                                word1, word2 = '@@@@@'.join(word1), '@@@@@'.join(word2)
                                table[word1][word2] = table[word1].setdefault(word2, 0) + 1
                                table[word2][word1] = table[word2].setdefault(word1, 0) + 1

                Collect.insert(({'key':key, 'value':keyDict} for key, keyDict in table.items()))

        self.Collect.remove({})
        filepathList = [os.path.join(dir_path, file_name) for (dir_path, dir_names, file_names) in os.walk('wikijson') for file_name in file_names]
        amount = math.ceil(len(filepathList)/self.cpus)
        filepathList = [filepathList[i:i + amount] for i in range(0, len(filepathList), amount)]
        processes = [mp.Process(target=cut_cal_and_insert, kwargs={'filepaths':filepathList[i]}) for i in range(self.cpus)]

        for process in processes:
            process.start()
        for process in processes:
            process.join()
        self.Collect.create_index([("key", pymongo.HASHED)])
        logging.info('finish kcm insert')

    def merge(self):
        logging.info('start merging kcm')
        # wordSet = list({keywordDict['key'] for keywordDict in self.Collect.find({}, {'_id':False})}) 
        wordSet = list({keywordDict['key'] for keywordDict in self.Collect.find({}, {'_id':False})}) 
        mergeCpus = 3
        amount = math.ceil(len(wordSet)/mergeCpus)
        wordSet = [wordSet[i:i + amount] for i in range(0, len(wordSet), amount)]

        @graceful_auto_reconnect
        def mergeKCMDict(wordSubset):
            db = MongoClient(self.uri).nlp
            Collect = db['kcm_{}'.format(self.lang)]
            fs = gridfs.GridFS(db)

            KCMCollect = MongoClient(self.uri).nlp.kcm_real
            result = defaultdict(dict)

            while wordSubset:
                key = wordSubset.pop()
                for keyCollect in Collect.find({'key':key}):
                    keyDict = keyCollect['value']
                    for keyOfkeydict, valueOfkeydict in keyDict.items():
                        result[key][keyOfkeydict] = result[key].setdefault(keyOfkeydict, 0) + valueOfkeydict
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                result[key] = [
                    key_and_partOfSpeech.split('@@@@@')+[count] 
                    for key_and_partOfSpeech, count in sorted(result[key].items(), key=lambda x:-x[1])
                ]
                # # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看
                # 沒加這行好像會佔很多記憶體，務必再實驗看看



                if len(result) >= 100000:
                    def Document_Generator():
                        for key, value in result.items():
                            payload = {
                                'key':key.split('@@@@@')[0],
                                'PartOfSpeech':key.split('@@@@@')[1],
                                'value':value
                            }
                            # The maximum BSON document size is 16 megabytes.
                            # So if document exceeds this limit
                            # use GridFS to store it.
                            print(deep_getsizeof(payload))
                            if deep_getsizeof(payload) >= 16777216:
                                fs.put(json.dumps(payload['value']), metadata={'key':payload['key'], 'PartOfSpeech':payload['PartOfSpeech']}, encoding='utf-8')
                            else:
                                yield payload

                    KCMCollect.insert(Document_Generator())
                    result = defaultdict(dict)

        processes = [mp.Process(target=mergeKCMDict, kwargs={'wordSubset':wordSet[i]}) for i in range(mergeCpus)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
                                        
        self.KCMCollect.create_index([("key", pymongo.HASHED)])
        logging.info('finish merging kcm')

    def get(self, keyword, amount):
        # GridFS query example
        # json.loads(fs.find_one({"filename": "david"}).read().decode('utf-8'))

        result = self.KCMCollect.find({'key':keyword}, {'_id':False}).limit(1)
        if result.count():
            return {**(result[0]), 'similarity':1}
        else:
            ngramKeyword = self.kcmNgram.find(keyword)
            if ngramKeyword:
                result = self.KCMCollect.find({'key':ngramKeyword}, {'_id':False}).limit(1)
                return {'key':ngramKeyword, 'value':result[0]['value'][:amount], 'similarity':self.kcmNgram.compare(keyword, ngramKeyword)}
            return {'key':ngramKeyword, 'value':[], 'similarity':0}