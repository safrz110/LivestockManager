# This file helps add the missing columns to the database

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('livestock', '0004_merge_species_breed_migrations'),
    ]

    operations = [
        # Add species_ref_id field if it doesn't exist
        migrations.AddField(
            model_name='animal',
            name='species_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='livestock.species'),
        ),
        # Add breed_ref_id field if it doesn't exist
        migrations.AddField(
            model_name='animal',
            name='breed_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='livestock.breed'),
        ),
    ]
