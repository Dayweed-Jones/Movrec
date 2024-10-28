# Generated by Django 4.1 on 2024-08-28 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_alter_list_movie_alter_list_user_mlratings'),
        ('recsys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CBSimilarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('similarity', models.DecimalField(decimal_places=7, max_digits=8)),
                ('movie_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cb_similarity_set_1', to='homepage.movies')),
                ('movie_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cb_similarity_set_2', to='homepage.movies')),
            ],
            options={
                'db_table': 'cb_similarity',
            },
        ),
    ]
