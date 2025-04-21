"""
Startup script for Render deployment to ensure the correct settings are used.
"""
import os
import sys

# Force-set critical environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'livestock_manager.settings'
os.environ['ALLOWED_HOSTS'] = '*,livestock-manager.onrender.com'

print("Startup script executed.", file=sys.stderr)
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}", file=sys.stderr)
print(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}", file=sys.stderr)
