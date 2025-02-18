# Generated by Django 4.1 on 2024-04-01 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='images',
            name='is_poster',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='movies',
            name='adult',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='movies',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='movies',
            name='release_date',
            field=models.DateField(),
        ),
    ]
