# Generated by Django 4.1 on 2024-08-29 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_rename_ml_user_mlratings_score_and_more'),
        ('recsys', '0003_colsimilarity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='COLSimilarity',
            new_name='CFSimilarity',
        ),
    ]