from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from opentelemetry import trace


load_dotenv()

def index(request):
    # Start a new span with the name "hello"
    return render(request, 'index.html')

@login_required
def hello(request):
    username = request.user.username
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("user") as span:
        span.set_attribute("user_first_name", request.user.username)
    return render(request, 'hello.html', {'username': username})