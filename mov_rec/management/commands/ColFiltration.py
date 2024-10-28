from django.core.management.base import BaseCommand
from model_training.CF_Filtration import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Calculation of item similarity")
        all_ratings = load_all_ratings()
        CF_Filtration(min_overlap=15, min_sim=0.1).build(all_ratings)
        print(all_ratings)