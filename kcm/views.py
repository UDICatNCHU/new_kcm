# -*- coding: utf-8 -*-
from django.http import JsonResponse
from djangoApiDec.djangoApiDec import queryString_required
from KCM.__main__ import KCM
from udic_nlp_API.settings_database import uri
kcmObject = KCM('cht', 'cht', uri=uri)

@queryString_required(['keyword'])
def kcm(request):
    """Generate list of term data source files
    Returns:
        if contains invalid queryString key, it will raise exception.
    """
    keyword = request.GET['keyword']

    result = kcmObject.get(keyword, int(request.GET['num']) if 'num' in request.GET else 10)
    return JsonResponse(result, safe=False)