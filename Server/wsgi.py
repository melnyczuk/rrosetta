"""
WSGI config for Server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
DEFAULT_SETTINGS_MODULE = "settings"

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

import django
django.setup() 

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
