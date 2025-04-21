"""
WSGI config for livestock_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Set correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestock_manager.settings')

# Print current environment variables for debugging
print("=== WSGI ENVIRONMENT VARIABLES ===", file=sys.stderr)
for key, value in os.environ.items():
    if key in ['DJANGO_SETTINGS_MODULE', 'PYTHONPATH', 'PATH']:
        print(f"{key}: {value}", file=sys.stderr)
print("================================", file=sys.stderr)

# Get the application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Print debug info after loading the application
print("=== DJANGO SETTINGS INFO ===", file=sys.stderr)
try:
    from django.conf import settings
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}", file=sys.stderr)
    print(f"DEBUG mode: {settings.DEBUG}", file=sys.stderr)
    print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}", file=sys.stderr)
    print(f"Static URL: {settings.STATIC_URL}", file=sys.stderr)
    print(f"Static Root: {settings.STATIC_ROOT}", file=sys.stderr)
except Exception as e:
    print(f"Error printing settings: {e}", file=sys.stderr)
print("==========================", file=sys.stderr)
