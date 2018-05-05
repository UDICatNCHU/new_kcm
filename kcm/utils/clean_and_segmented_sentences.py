# for zh 
from udicOpenData.stopwords import rmsw
from opencc import OpenCC
from itertools import chain
openCC = OpenCC('s2t')

# for th
import nltk 
from nltk.corpus import stopwords 
th_stopwords = set(stopwords.words('thai'))

# for en
###############
# coming soon #
###############

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
	elif lang == 'en':
		pass
	elif lang == 'th':
		pass