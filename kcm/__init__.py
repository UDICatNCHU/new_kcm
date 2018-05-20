#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymongo, os, math, json_lines, logging, sys, json, gridfs
import multiprocessing as mp
from pymongo import MongoClient
from ngram import NGram
from kcm.utils.clean_and_segmented_sentences import clean_and_segmented_sentences
from kcm.utils.graceful_auto_reconnect import graceful_auto_reconnect
from pympler.asizeof import asizeof
from collections import defaultdict
from itertools import combinations, chain
logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='buildKCM.log', level=logging.INFO)


class KCM(object):
	def __init__(self, input_dir='wikijson', lang='zh', uri=None):
		self.input_dir = input_dir
		self.lang = lang
		self.uri = uri
		self.db = MongoClient(self.uri)['nlp_{}'.format(self.lang)]
		self.Collect = self.db['kcm_intermediate']
		self.KCMCollect = self.db['kcm']
		self.fs = gridfs.GridFS(self.db)

		# prevent it from taking up all the cpus and make MongoDB dead.
		self.cpus = math.ceil(mp.cpu_count() * 0.7)
		self.mergeCpus = math.ceil(mp.cpu_count() * 0.1)

		# use ngram for searching
		self.kcmNgram = NGram((i['key'] for i in self.KCMCollect.find({}, {'key':1, '_id':False})))

	def build(self):
		# graceful_auto_reconnect is used to handle Mongo Connection issue.
		# when Mongo is too busy, it somehow frozen and restart mongod.service
		# which will cause connection issue
		# so need a decorator to wait and reconnect manually.
		@graceful_auto_reconnect
		def cut_cal_and_insert(filepaths):
			# Each process need independent Mongo Client
			# or it may raise Deadlock in Mongo.
			Collect = MongoClient(self.uri)['nlp_{}'.format(self.lang)]['kcm_intermediate']

			for index, filepath in enumerate(filepaths):
				if index%10 == 0:
					logging.info("already processed %d files" % index)
				table = defaultdict(dict)

				with open(filepath, 'r') as f:
					for article in json_lines.reader(f):
						sentences = clean_and_segmented_sentences(self.lang, article)
						for sentence in sentences:
							sentence = list(sentence)
							if len(sentence) <= 1: continue
							start, end = [(('<start>', 'xx'), sentence[0])], [(sentence[-1], ('<end>', 'xx'))]
							combinations_with_startAndEnd = chain(start, combinations(sentence, 2), end)

							for word_couple in combinations_with_startAndEnd:
								# word_couple is supposed to be two word_and_partofspeech, but it somehow has null in it...
								# word_and_partofspeech's type is List
								# [word, part of speech]
								# But Mongo cannot use tuple or List as key
								# so i just concatenate it with <cut> for the sake of convineint
								# and split it after the insertion.

								word1_and_partofspeech, word2_and_partofspeech = word_couple
								word1_and_partofspeech, word2_and_partofspeech = '<cut>'.join(word1_and_partofspeech), '<cut>'.join(word2_and_partofspeech)

								# bson.errors.InvalidDocument: key '.' must not contain '.'
								# so replace . into ''
								word1_and_partofspeech, word2_and_partofspeech = word1_and_partofspeech.replace('.', ''), word2_and_partofspeech.replace('.', '')								

								table[word1_and_partofspeech][word2_and_partofspeech] = table[word1_and_partofspeech].setdefault(word2_and_partofspeech, 0) + 1
								table[word2_and_partofspeech][word1_and_partofspeech] = table[word2_and_partofspeech].setdefault(word1_and_partofspeech, 0) + 1
				Collect.insert(({'key':key, 'value':keyDict} for key, keyDict in table.items()))

		# empty first
		self.KCMCollect.remove({})
		self.Collect.remove({})
		self.db.drop_collection('fs.chunks')
		self.db.drop_collection('fs.files')
		logging.info('finishing emtpy Collection and fileSystem')
		
		filepathList = [os.path.join(dir_path, file_name) for (dir_path, dir_names, file_names) in os.walk(self.input_dir) for file_name in file_names]

		# If self.cpus > len(filepathList)
		# then amount would be zero
		# which would occurs IndexError: list index out of range
		# from filepathList array.
		if len(filepathList) < self.cpus:
			self.cpus = len(filepathList)
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
		wordSet = list({keywordDict['key'] for keywordDict in self.Collect.find({}, {'_id':False})}) 
		amount = math.ceil(len(wordSet)/self.mergeCpus)
		wordSet = [wordSet[i:i + amount] for i in range(0, len(wordSet), amount)]

		@graceful_auto_reconnect
		def mergeKCMDict(wordSubset):
			# Each process need independent Mongo Client
			# or it may raise Deadlock in Mongo.
			db = MongoClient(self.uri)['nlp_{}'.format(self.lang)]
			Collect = db['kcm_intermediate']
			KCMCollect = db['kcm']
			fs = gridfs.GridFS(db)

			result = defaultdict(dict)

			while wordSubset:
				key = wordSubset.pop()
				for keyCollect in Collect.find({'key':key}):
					keyDict = keyCollect['value']
					for keyOfkeydict, valueOfkeydict in keyDict.items():
						result[key][keyOfkeydict] = result[key].setdefault(keyOfkeydict, 0) + valueOfkeydict

				# Dict will take much mem space than List
				# so use list comprehension to do transformation.
				result[key] = [
					key_and_partOfSpeech.split('<cut>')+[count] 
					for key_and_partOfSpeech, count in sorted(result[key].items(), key=lambda x:-x[1])
				]

				# It would take up too much RAM if we merge all Document into one list and insert once
				# so we wait till list contains 5000 words and then flush them into MongoDB
				if len(result) >= 5000:
					def Document_Generator():
						for key, value in result.items():
							payload = {
								'key':key.split('<cut>')[0],
								'PartOfSpeech':key.split('<cut>')[1],
								'value':value
							}
							# The maximum BSON document size is 16 megabytes.
							# So if document exceeds this limit
							# use GridFS to store it.
							if asizeof(payload) >= 16777216:
								fs.put(json.dumps(payload['value']), filename=payload['key'], contentType=payload['PartOfSpeech'], encoding='utf-8')
							else:
								yield payload

					KCMCollect.insert(Document_Generator())
					result = defaultdict(dict)

			# We have a 5000 insert threshold up there.
			# so please remember to insert the rest of the list which is less than 5000
			KCMCollect.insert(Document_Generator())

		processes = [mp.Process(target=mergeKCMDict, kwargs={'wordSubset':wordSet[i]}) for i in range(self.mergeCpus)]
		for process in processes:
			process.start()
		for process in processes:
			process.join()
		self.KCMCollect.create_index([("key", pymongo.HASHED)])
		
		# List the names of all files stored in this instance of GridFS.
		# An index on {filename: 1, uploadDate: -1} will automatically be created when this method is called the first time.
		self.fs.list()

		# KCMCollect is our final collections
		# Collect is just a intermediate collections
		# so drop it after finishing merge.
		self.Collect.drop()
		logging.info('finish merging kcm')

	@graceful_auto_reconnect
	def get(self, keyword, amount=10, keyFlag=[], valueFlag=[]):
		def valueFlagFind(result):
			result['value'] = [i for i in result['value'] if i[1] in valueFlag or valueFlag == []]
			result['value'].sort(key=lambda x:x[2], reverse=True)
			result['value'] = result['value'][:amount]		
			return result
		def keyFlagFind(OriginKeyword):
			NgramKeyword = self.kcmNgram.find(OriginKeyword) if self.kcmNgram.find(OriginKeyword) else None
			result = {'key':NgramKeyword, 'similarity':self.kcmNgram.compare(OriginKeyword, NgramKeyword), 'PartOfSpeech':[], 'value':[]}
			useGridFS = False

			cursorList = self.KCMCollect.find({'key':NgramKeyword}, {'_id':False}).limit(1)
			# if Collection found, but not very sure (similarity not equal 1)
			# then also check GridFS
			# whether there's a complete match or not
			# if does, use it. else, use ngram as query and return result from Collections.
			if result['similarity'] != 1:
				tmpCursorList = self.fs.find({"filename": OriginKeyword}).limit(1)
				if tmpCursorList.count():
					result['key'], result['similarity'] = OriginKeyword, 1
					useGridFS = True
					cursorList = tmpCursorList
			for cursor in cursorList:
				if useGridFS: cursor = {'PartOfSpeech':cursor.contentType, 'value':json.loads(self.fs.get(cursor._id).read().decode('utf-8'))}
				if cursor['PartOfSpeech'] in keyFlag or not keyFlag:
					result['value'] += cursor['value']
					result['PartOfSpeech'].append(cursor['PartOfSpeech'])
			return result
		return valueFlagFind(keyFlagFind(keyword))