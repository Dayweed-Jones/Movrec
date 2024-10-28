# Generated by Django 4.1 on 2024-08-29 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_alter_list_movie_alter_list_user_mlratings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mlratings',
            old_name='ml_user',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='mlratings',
            old_name='rating',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='movies',
            unique_together={('name', 'release_date')},
        ),
    ]