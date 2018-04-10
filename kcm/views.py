# -*- coding: utf-8 -*-
from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from kcm import KCM
from udic_nlp_API.settings_database import uri
kcmObject = KCM(lang='zh', uri=uri)

@queryString_required(['keyword'])
def kcm(request):
    keyword = request.GET['keyword']
    result = kcmObject.get(keyword=keyword, amount=int(request.GET['num']) if 'num' in request.GET else 10, keyFlag=request.GET['keyFlag'].split() if 'keyFlag' in request.GET else [], valueFlag=request.GET['valueFlag'].split() if 'valueFlag' in request.GET else [])
    return JsonResponse(result, safe=False)