import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestock_manager.settings')
django.setup()

from django.db import connection

def clean_migrations():
    with connection.cursor() as cursor:
        # First, check if HealthRecord table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='livestock_healthrecord';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("Dropping the existing HealthRecord table...")
            cursor.execute("DROP TABLE IF EXISTS livestock_healthrecord;")
            print("Table dropped successfully.")
        
        # Remove any migration history related to HealthRecord
        cursor.execute("SELECT id, app, name FROM django_migrations WHERE app='livestock' AND name LIKE '%health%';")
        migrations = cursor.fetchall()
        
        if migrations:
            print("Removing migration history for HealthRecord...")
            for migration in migrations:
                print(f"Removing migration: {migration[2]}")
                cursor.execute("DELETE FROM django_migrations WHERE id = %s;", [migration[0]])
            print("Migration history cleaned.")
        else:
            print("No HealthRecord migrations found in history.")
            
        print("\nYou can now run: python manage.py makemigrations")
        print("Then: python manage.py migrate")

if __name__ == "__main__":
    clean_migrations()
