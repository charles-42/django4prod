# settings/default.py

from .base import *
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# False if not in os.environ because of casting above
DJANGO_ENV = os.getenv('DJANGO_ENV')

if DJANGO_ENV == "development":
    DEBUG = True
else:
    DEBUG = False

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = os.getenv('SECRET_KEY', default='defaultsecret')

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', default='*')]


# Database

if DJANGO_ENV == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('NAME'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = ["https://django-on-azure-app-beniac.azurewebsites.net"]

# Monitoring

MONITORING = os.getenv('MONITORING', default=False)

if MONITORING is True:
    # Configuration de l'exportateur Azure Monitor
    trace_exporter = AzureMonitorTraceExporter(
        connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    )

    # Configuration du Tracer Provider
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    # Définir le fournisseur de traceur global
    trace.set_tracer_provider(trace_provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer("my.tracer.name")

    if DJANGO_ENV == 'production':
        Psycopg2Instrumentor().instrument()

    logger = logging.getLogger(__name__)

    # # # # Instrumentation de Django
    DjangoInstrumentor().instrument()
