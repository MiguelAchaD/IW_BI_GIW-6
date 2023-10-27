from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "index.html", context)

def logIn(request):
    context = {}
    return render(request, "accounts\\logIn.html", context)

def register(request):
    context = {}
    return render(request, "accounts\\register.html", context)