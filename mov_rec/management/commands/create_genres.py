from django.core.management.base import BaseCommand
from homepage.models import Genres  # Import your models here


class Command(BaseCommand):
    help = "add genres"

    def handle(self, *args, **options):
        genres = [
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "History",
            "Horror",
            "Music",
            "Mystery",
            "Romance",
            "Science Fiction",
            "TV Movie",
            "Thriller",
            "War",
            "Western",
        ]
        for g in genres:
            if not Genres.exists(g):
                genre = Genres.objects.create(genre=g)
                genre.save()