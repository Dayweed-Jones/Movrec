import pandas as pd
from django.core.management.base import BaseCommand
from homepage.models import (
    Movies,
    MLRatings,
    Credits
) 


class Command(BaseCommand):
    help = "populate db"

    def handle(self, *args, **options):
        # MLRatings.objects.all().delete()
        # df = pd.read_csv("New_ratings.csv")
        # for index, row in df.iterrows():
        #     rating = MLRatings(movie_id=row["MyId"], ml_user=row["userId"], rating=int(row["rating"]*2))
        #     rating.save()
        print(Credits.objects.filter(movie_id=2569, department="Directing"))
