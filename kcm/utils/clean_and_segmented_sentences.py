from udicOpenData.stopwords import rmsw

def clean_and_segmented_sentences(lang, article):
	if lang == 'zh-TW':
		return (rmsw(i) for i in article.strip().split('。'))