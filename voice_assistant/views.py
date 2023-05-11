from django.http import JsonResponse
from django.shortcuts import render

import utils


def home(request):
    text = ""
    search_results = []
    if request.method == 'POST' and 'record' in request.POST:
        text = utils.recognize_speech()
        search_results = utils.search_keywords_in_db(text)
        return JsonResponse({'text': text, 'search_results': search_results})
    return render(request, 'home.html', {'text': text, 'search_results': search_results})




