from django.http import Http404
from django.shortcuts import render

# Create your views here.
from .models import Result


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def results(request):
    results = Result.objects.all()
    if not results:
        raise Http404("Results does not exist")
    return render(request, 'main/results.html', {'all_results_list': results})
