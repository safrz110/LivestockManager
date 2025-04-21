# Generated manually

from django.db import migrations

def add_default_species_and_breeds(apps, schema_editor):
    Species = apps.get_model('livestock', 'Species')
    Breed = apps.get_model('livestock', 'Breed')
    
    # Create default species
    cow = Species.objects.create(name='Cow')
    buffalo = Species.objects.create(name='Buffalo')
    goat = Species.objects.create(name='Goat')
    sheep = Species.objects.create(name='Sheep')
    pig = Species.objects.create(name='Pig')
    chicken = Species.objects.create(name='Chicken')
    
    # Create default breeds for Cows
    Breed.objects.create(name='Holstein', species=cow)
    Breed.objects.create(name='Jersey', species=cow)
    Breed.objects.create(name='Brown Swiss', species=cow)
    Breed.objects.create(name='Hereford', species=cow)
    Breed.objects.create(name='Angus', species=cow)
    
    # Create default breeds for Buffalos
    Breed.objects.create(name='Murrah', species=buffalo)
    Breed.objects.create(name='Nili-Ravi', species=buffalo)
    Breed.objects.create(name='Surti', species=buffalo)
    
    # Create default breeds for Goats
    Breed.objects.create(name='Boer', species=goat)
    Breed.objects.create(name='Alpine', species=goat)
    Breed.objects.create(name='Nubian', species=goat)
    Breed.objects.create(name='Saanen', species=goat)
    
    # Create default breeds for Sheep
    Breed.objects.create(name='Merino', species=sheep)
    Breed.objects.create(name='Suffolk', species=sheep)
    Breed.objects.create(name='Dorper', species=sheep)
    
    # Create default breeds for Pigs
    Breed.objects.create(name='Yorkshire', species=pig)
    Breed.objects.create(name='Duroc', species=pig)
    Breed.objects.create(name='Landrace', species=pig)
    
    # Create default breeds for Chickens
    Breed.objects.create(name='Leghorn', species=chicken)
    Breed.objects.create(name='Rhode Island Red', species=chicken)
    Breed.objects.create(name='Plymouth Rock', species=chicken)

def remove_default_species_and_breeds(apps, schema_editor):
    Species = apps.get_model('livestock', 'Species')
    Species.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0002_create_species_breed_tables'),
    ]

    operations = [
        migrations.RunPython(add_default_species_and_breeds, remove_default_species_and_breeds),
    ]
