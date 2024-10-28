# Generated by Django 4.1 on 2024-04-12 16:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_alter_genres_table_alter_ratings_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
