# Generated by Django 5.0.4 on 2025-04-14 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0006_supportrequest_remove_notification_related_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='animal_expertise',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with this email already exists.'}, max_length=254, unique=True),
        ),
    ]
