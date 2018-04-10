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

def clean_and_segmented_sentences(lang, article):
	if lang == 'zh':
		for i in article['text'].split('。'):
			seg = rmsw(openCC.convert(i), flag=True)
			seg = peek(seg)
			if seg is None:
				continue
			else:
				boolean, seg = seg
				yield seg

		# return (rmsw(openCC.convert(i), flag=True) for i in article['text'].split('。'))