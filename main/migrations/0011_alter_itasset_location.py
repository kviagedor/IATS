# Generated by Django 5.0.3 on 2024-05-15 03:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_itasset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itasset',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.location'),
        ),
    ]
