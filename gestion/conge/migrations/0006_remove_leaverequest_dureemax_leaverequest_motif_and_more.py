# Generated by Django 5.0.4 on 2024-07-18 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conge', '0005_leaverequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='dureemax',
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='motif',
            field=models.TextField(default='Pas de raison specifique'),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='statut',
            field=models.CharField(default='En attente', max_length=100),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='type_conge',
            field=models.CharField(max_length=100),
        ),
    ]
