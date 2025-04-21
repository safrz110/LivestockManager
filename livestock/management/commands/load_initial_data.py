from django.core.management.base import BaseCommand
from livestock.models import Species, Breed

INITIAL_DATA = {
    'Cattle': ['Holstein', 'Angus', 'Hereford', 'Jersey', 'Brahman'],
    'Goat': ['Boer', 'Nubian', 'Alpine', 'Saanen', 'LaMancha'],
    'Sheep': ['Merino', 'Suffolk', 'Dorper', 'Romney', 'Texel'],
    'Pig': ['Yorkshire', 'Duroc', 'Hampshire', 'Berkshire', 'Landrace'],
    'Poultry': ['Broiler', 'Layer', 'Dual Purpose', 'Heritage', 'Game']
}

class Command(BaseCommand):
    help = 'Load initial species and breeds data'

    def handle(self, *args, **kwargs):
        for species_name, breeds in INITIAL_DATA.items():
            species, _ = Species.objects.get_or_create(name=species_name)
            for breed_name in breeds:
                Breed.objects.get_or_create(
                    species=species,
                    name=breed_name
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
