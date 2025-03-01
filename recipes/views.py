from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'recipes/index.html', context=context_dict)