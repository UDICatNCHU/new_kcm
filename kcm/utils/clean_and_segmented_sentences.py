# ja
# MeCab has some bug
# so i cannot put these import statement into ja function scope ...
# TH: to install pythainlp for stopwords and segmentation, please install by the command line
# pip install pythainlp
import MeCab
mecab = MeCab.Tagger("-Ochasen")

def clean_and_segmented_sentences(lang, article):
	""" Do segmentation and removing stopwords for a wiki page

	Parameters
	----------
	lang : {str}. is the same abbreviation as wiki use
	article : {str}. plain text of wiki page. In kcm/__init__.py, var article is the plain text of wiki page for clean_and_segmented_sentences function

	Returns
	-------
	seg : {generator}, shape (numbers of sentences in an article, numbers of words in a sentence)
	An 2d array which contains bunches of segmentations of a sentence.
	e.g., [
		[['cake', 'n'], ['food', 'n']]
		...
		...
		...
	]
	"""
	if lang == 'zh':
		return zh(article)
	elif lang == 'th':
		return th(article)
	elif lang == 'en':
		pass
	elif lang == 'ja':
		return ja(article)

def zh(article):
	# for zh 
	from udicOpenData.stopwords import rmsw
	from opencc import OpenCC
	from itertools import chain
	openCC = OpenCC('s2t')

	def peek(iterable):
		try:
			first = next(iterable)
		except StopIteration:
			return None
		return True, chain([first], iterable)

	for i in article['text'].split('。'):
		seg = rmsw(openCC.convert(i), flag=True)
		seg = peek(seg)
		if seg is None:
			continue
		else:
			boolean, seg = seg
			yield seg

def th(article):
	# for th
	from pythainlp.corpus import stopwords
	from pythainlp.tokenize import word_tokenize
	from pythainlp.tag import pos_tag
	thstopwords = stopwords.words('thai') # a list of Thai stopwords
# 	test = word_tokenize('วันนี้อากาศดี',engine='newmm')        # text = 'Today has a good weather' return type as list ['วันนี้', 'อากาศ', 'ดี']
# 	POSlist = pos_tag(test,engine='old')			# pos_tag function input as a list of tokenized words ex. ['วันนี้', 'อากาศ', 'ดี'] and return [('วันนี้', 'NCMN'), ('อากาศ', 'NCMN'), ('ดี', 'VATT')]
	return

def ja(article):
	for line in article.split('。'):
		line = line.strip()
		if line:
			yield (i.split('\t')[0] for i in mecab.parse(line).split('\n')[:-2])
