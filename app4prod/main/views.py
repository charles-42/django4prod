from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv

load_dotenv()

def index(request):
    DJANGO_ENV = os.getenv('DJANGO_ENV')
    return render(request, 'index.html',{'DJANGO_ENV': DJANGO_ENV})

@login_required
def hello(request):
    username = request.user.username
    return render(request, 'hello.html', {'username': username})