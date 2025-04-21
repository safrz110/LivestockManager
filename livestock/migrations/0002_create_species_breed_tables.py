# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Species',
            },
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breeds', to='livestock.species')),
            ],
            options={
                'unique_together': {('name', 'species')},
            },
        ),
        migrations.AddField(
            model_name='animal',
            name='species_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='livestock.species'),
        ),
        migrations.AddField(
            model_name='animal',
            name='breed_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='livestock.breed'),
        ),
    ]
