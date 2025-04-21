from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion

def backfill_health_records(apps, schema_editor):
    """Fix any existing health records that might be missing data"""
    HealthRecord = apps.get_model('livestock', 'HealthRecord')
    
    # Set defaults for existing records
    HealthRecord.objects.filter(record_type__isnull=True).update(record_type='checkup')
    HealthRecord.objects.filter(title__isnull=True).update(title='Health Record')
    HealthRecord.objects.filter(description__isnull=True).update(description='No description provided')
    
    # Add current date for any records missing dates
    for record in HealthRecord.objects.filter(record_date__isnull=True):
        record.record_date = django.utils.timezone.now().date()
        record.save()

class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0001_initial'),  # This will depend on your current migration
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(blank=True, choices=[('vaccination', 'Vaccination'), ('treatment', 'Treatment'), ('checkup', 'Regular Checkup'), ('other', 'Other')], default='checkup', max_length=20, null=True)),
                ('record_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, default='No description provided', null=True)),
                ('medications', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('performed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='livestock.animal')),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.RunPython(backfill_health_records, migrations.RunPython.noop),
    ]
