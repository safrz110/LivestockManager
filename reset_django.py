import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestock_manager.settings')
django.setup()

from django.db import connection
import os
import shutil

def clean_migrations():
    """Clean up migration files and database entries related to problematic migrations"""
    
    # Get the migrations directory path
    migrations_dir = os.path.join('livestock', 'migrations')
    
    # Look for the problematic migration file
    problematic_file = os.path.join(migrations_dir, 'reset_health_records.py')
    
    # Delete the problematic file if it exists
    if os.path.exists(problematic_file):
        print(f"Removing problematic migration file: {problematic_file}")
        os.remove(problematic_file)
        
        # Also remove the compiled .pyc file if it exists
        pyc_file = problematic_file + 'c'
        if os.path.exists(pyc_file):
            os.remove(pyc_file)
    else:
        print("Problematic migration file not found.")
    
    # Check and clean the database migrations table if needed
    with connection.cursor() as cursor:
        # Check if HealthRecord table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='livestock_healthrecord';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("Checking for problematic migrations in database...")
            cursor.execute("SELECT id, name FROM django_migrations WHERE app='livestock' AND name='reset_health_records';")
            bad_migrations = cursor.fetchall()
            
            if bad_migrations:
                print(f"Found {len(bad_migrations)} problematic migration entries. Removing them...")
                for migration in bad_migrations:
                    cursor.execute("DELETE FROM django_migrations WHERE id = %s;", [migration[0]])
                print("Removed problematic migration entries from database.")
            else:
                print("No problematic migration entries found in database.")
    
    print("\nComplete! Now you can run:")
    print("1. python manage.py makemigrations livestock")
    print("2. python manage.py migrate livestock")

if __name__ == "__main__":
    clean_migrations()
