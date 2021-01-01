"""
WSGI config for movie_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from configurations.wsgi import get_wsgi_application
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE'))
os.environ.setdefault('DJANGO_CONFIGURATION', os.environ.get('DJANGO_CONFIGURATION'))

application = get_wsgi_application()
