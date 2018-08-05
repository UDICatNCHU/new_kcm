# -*- coding: utf-8 -*-
from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from kcm import KCM
from udic_nlp_API.settings_database import uri

MULTILANGUAGE_MODEL = {
	'zh': KCM(lang='zh', uri=uri, ngram=False),
	# 'th': KCM(lang='th', uri=uri, ngram=False)
}

@queryString_required(['lang', 'keyword'])
def kcm(request):
	keyword = request.GET['keyword']
	lang = request.GET['lang']
	result = MULTILANGUAGE_MODEL[lang].get(keyword=keyword, amount=int(request.GET['num']) if 'num' in request.GET else 10, keyFlag=request.GET['keyFlag'].split() if 'keyFlag' in request.GET else [], valueFlag=request.GET['valueFlag'].split() if 'valueFlag' in request.GET else [])
	return JsonResponse(result, safe=False)

@queryString_required(['lang', 'keyword'])
def search(request):
	keyword = request.GET['keyword']
	lang = request.GET['lang']
	threshold = float(request.GET['threshold']) if 'threshold' in request.GET else 0
	num = int(request.GET['num']) if 'num' in request.GET else 10
	return JsonResponse(MULTILANGUAGE_MODEL[lang].kcmNgram.search(keyword, threshold=threshold)[:num], safe=False)
