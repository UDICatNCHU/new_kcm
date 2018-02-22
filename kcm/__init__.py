#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymongo, multiprocessing, os, threading, math
from pymongo import MongoClient
from threading import Thread
from ngram import NGram
from udicOpenData.stopwords import rmsw
from kcm.utils.clean_and_segment import clean_and_segment
from collections import defaultdict


class KCM(object):
    def __init__(self, lang='zh-TW', input_dir, uri=None):
        self.lang = lang
        self.input_dir = input_dir

        self.client = MongoClient(uri)
        self.db = self.client['nlp']
        self.Collect = self.db['kcm_{}'.format(self.lang)]

        self.threadLock = threading.Lock()
        self.result = defaultdict(dict)
        # ngram search
        self.kcmNgram = NGram((i['key'] for i in self.Collect.find({}, {'key':1, '_id':False})))

    def build(self):
        # # if self.lang == 'cht':
        # subprocess.call(['opencc', '-i', 'wikijson/wiki.txt.all', '-o', 'wikijson/wiki.txt.all.{}'.format(self.lang)])
        def cut_cal_and_insert(filepaths):
            table = defaultdict(dict)
            for filepath in filepaths:
                with open(filepath, 'r') as f:
                    for article in json_lines.reader(f):
                        sentences = clean_and_segmented_sentences(self.lang, article)
                        for sentence in sentences:
                            for word1, word2 in combinations(sentence, 2):
                                table[wor1][word2] = table[word1].setdefault(word2) + 1
                                table[wor2][word1] = table[word2].setdefault(word1) + 1
            self.threadLock.acquire()
            for key, keydict in table.items():
                for keyOfkeydict, valueOfkeydict in keydict.items():
                    self[key][keyOfkeydict] = self.result[key].setdefault(keyOfkeydict, 0) + valueOfkeydict
            self.threadLock.release()
                        
        filepathList = [os.path.join(dir_path, file_name) for (dir_path, dir_names, file_names) in os.walk('wikijson') for file_name in file_names]
        cpus = multiprocessing.cpu_count()
        amount = math.ceil(len(filepathList)/cpus)
        filepathList = [filepathList[i:i + amount] for i in range(0, len(filepathList), amount)]
        workers = [threading.Thread(target=cut_cal_and_insert, kwargs={'filepaths':filepathList[i]}) for i in range(cpus)]

        for thread in workers:
           thread.start()
        for thread in workers:
            thread.join()

        self.Collect.remove({})
        self.Collect.insert((
            {
                'key':key,
                'value':sorted(value.items(), key=lambda x:-x[1])
            } for key, value in table.items()
        ))
        self.Collect.create_index([("key", pymongo.HASHED)])

    def get(self, keyword, amount):
        result = self.Collect.find({'key':keyword}, {'_id':False}).limit(1)
        if result.count():
            return {**(result[0]), 'similarity':1}
        else:
            ngramKeyword = self.kcmNgram.find(keyword)
            if ngramKeyword:
                result = self.Collect.find({'key':ngramKeyword}, {'_id':False}).limit(1)
                return {'key':ngramKeyword, 'value':result[0]['value'][:amount], 'similarity':self.kcmNgram.compare(keyword, ngramKeyword)}
            return {'key':ngramKeyword, 'value':[], 'similarity':0}