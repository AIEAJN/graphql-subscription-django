"""
ASGI config for lunastarter project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""



import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
from django_ws import get_websocket_application


application = get_websocket_application()

       