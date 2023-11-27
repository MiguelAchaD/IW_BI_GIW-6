from django.contrib.sites.requests import RequestSite

def getURL(request):
    current_site = RequestSite(request)
    return f"http://{current_site.domain}"
