"""
Configurações para desenvolvimento
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# BrowsableAPI para desenvolvimento
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

# Email para console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'