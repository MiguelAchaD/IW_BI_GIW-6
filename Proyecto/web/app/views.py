from django.http import HttpResponse
from utils import getTemplate

def index(request):
    return HttpResponse(getTemplate("web\\app\\templates\\index.html"))