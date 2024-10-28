from django.core.management.base import BaseCommand
from recsys.models import MLRatings
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):
        ml_ratings = pd.read_csv("New_ratings.csv")
        ml_ratings = ml_ratings.drop("row", axis=1)
        cols = {'userId': 'user', 'rating': 'score', 'MyId': 'movie'}
        ml_ratings = ml_ratings.rename(columns=cols)
        for _, rating in ml_ratings.iterrows():
            rating = MLRatings(user_id=rating["userId"],score=int(rating["rating"]*2), movie=rating["MyID"] )