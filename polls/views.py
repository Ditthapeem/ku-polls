from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def index(request):
    """Display an index for this app.

    Parameters:
            request - an HttpRequest containing the client's request data
    Return:
        an HttpResponse
    """
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
