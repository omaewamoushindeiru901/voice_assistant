from django.http import JsonResponse
from django.shortcuts import render

import utils


def home(request):
    text = ""
    search_results = []
    found = False
    if request.method == 'POST' and 'record' in request.POST:
        text = utils.recognize_speech()
        search_results, found = utils.search_keywords_in_db(text)
        return JsonResponse({'text': text, 'search_results': search_results, 'found': found})
    return render(request, 'home.html', {'text': text, 'search_results': search_results, 'found': found})





