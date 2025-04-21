# Generated manually to solve migration conflicts

from django.db import migrations

class Migration(migrations.Migration):
    """
    This migration merges the conflicting migrations:
    - 0002_add_species_breed_models
    - 0003_add_default_species_and_breeds
    """

    dependencies = [
        ('livestock', '0002_add_species_breed_models'),
        ('livestock', '0003_add_default_species_and_breeds'),
    ]

    operations = [
        # No operations needed, this just merges the two migration branches
    ]
