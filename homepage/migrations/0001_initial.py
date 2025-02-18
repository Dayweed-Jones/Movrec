# Generated by Django 4.1 on 2024-04-01 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('adult', models.BooleanField(blank=True, null=True)),
                ('release_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_poster', models.BooleanField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.movies')),
            ],
            options={
                'db_table': 'images',
            },
        ),
    ]
