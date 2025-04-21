"""
Print debug information about the Django settings and environment.
Add to the project to help diagnose deployment issues.
"""

import os
import sys
import django
from django.conf import settings

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestockManager.settings')
django.setup()

# Print debug information
print("=== DEBUG INFORMATION ===")
print(f"Django version: {django.get_version()}")
print(f"Python version: {sys.version}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DEBUG setting: {settings.DEBUG}")
print("Environment variables:")
for key, value in os.environ.items():
    if key.startswith(('DJANGO_', 'RENDER_', 'DATABASE_URL')):
        print(f"  {key}: {'*****' if 'SECRET' in key else value}")
print("========================")
