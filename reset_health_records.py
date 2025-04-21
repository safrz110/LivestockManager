import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestock_manager.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS livestock_healthrecord;")
    print("Health Record table dropped. Run migrations to recreate it.")
