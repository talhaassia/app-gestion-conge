# Generated by Django 5.0.4 on 2024-07-18 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conge', '0003_personne_is_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='conge',
            name='traitement',
            field=models.BooleanField(default=False),
        ),
    ]