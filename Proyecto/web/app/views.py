from django.http import HttpResponse
from utils import getTemplate
from django.template import Context

def index(request):
    return HttpResponse(getTemplate("web\\app\\templates\\index.html", Context()))

def logIn(request):
    return HttpResponse(getTemplate("web\\app\\templates\\accounts\\logIn.html", Context()))

def register(request):
    return HttpResponse(getTemplate("web\\app\\templates\\accounts\\register.html", Context()))