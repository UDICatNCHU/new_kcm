from udicOpenData.stopwords import rmsw
from opencc import OpenCC
openCC = OpenCC('s2t')
def clean_and_segmented_sentences(lang, article):
	if lang == 'zh_TW':
		return (rmsw(openCC.convert(i), flag=True) for i in article['text'].split('。'))