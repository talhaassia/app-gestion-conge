# Generated by Django 5.0.4 on 2024-07-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conge', '0002_conge_remove_employee_groups_remove_employee_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='is_director',
            field=models.BooleanField(default=False),
        ),
    ]
