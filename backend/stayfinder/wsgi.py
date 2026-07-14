"""WSGI config for StayFinder project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stayfinder.settings')
application = get_wsgi_application()
