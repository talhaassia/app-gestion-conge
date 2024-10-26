# Generated by Django 5.0.4 on 2024-07-18 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conge', '0004_conge_traitement'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_conge', models.CharField(max_length=50)),
                ('dureemax', models.IntegerField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('personne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]