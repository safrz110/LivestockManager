from django.core.management.base import BaseCommand
from livestock.models import Species, Breed

class Command(BaseCommand):
    help = 'Populate the database with default species and breeds'

    def handle(self, *args, **kwargs):
        # Check if we already have species
        if Species.objects.exists():
            self.stdout.write(self.style.WARNING('Species already exist. Skipping population.'))
            return
        
        # Create default species
        self.stdout.write('Creating species...')
        cow = Species.objects.create(name='Cow')
        buffalo = Species.objects.create(name='Buffalo')
        goat = Species.objects.create(name='Goat')
        sheep = Species.objects.create(name='Sheep')
        pig = Species.objects.create(name='Pig')
        chicken = Species.objects.create(name='Chicken')
        
        # Create breeds for each species
        self.stdout.write('Creating breeds for Cow...')
        Breed.objects.create(name='Holstein', species=cow)
        Breed.objects.create(name='Jersey', species=cow)
        Breed.objects.create(name='Brown Swiss', species=cow)
        Breed.objects.create(name='Hereford', species=cow)
        Breed.objects.create(name='Angus', species=cow)
        
        self.stdout.write('Creating breeds for Buffalo...')
        Breed.objects.create(name='Murrah', species=buffalo)
        Breed.objects.create(name='Nili-Ravi', species=buffalo)
        Breed.objects.create(name='Surti', species=buffalo)
        
        self.stdout.write('Creating breeds for Goat...')
        Breed.objects.create(name='Boer', species=goat)
        Breed.objects.create(name='Alpine', species=goat)
        Breed.objects.create(name='Nubian', species=goat)
        Breed.objects.create(name='Saanen', species=goat)
        
        self.stdout.write('Creating breeds for Sheep...')
        Breed.objects.create(name='Merino', species=sheep)
        Breed.objects.create(name='Suffolk', species=sheep)
        Breed.objects.create(name='Dorper', species=sheep)
        
        self.stdout.write('Creating breeds for Pig...')
        Breed.objects.create(name='Yorkshire', species=pig)
        Breed.objects.create(name='Duroc', species=pig)
        Breed.objects.create(name='Landrace', species=pig)
        
        self.stdout.write('Creating breeds for Chicken...')
        Breed.objects.create(name='Leghorn', species=chicken)
        Breed.objects.create(name='Rhode Island Red', species=chicken)
        Breed.objects.create(name='Plymouth Rock', species=chicken)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated species and breeds!'))
