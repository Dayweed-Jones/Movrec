from django.core.management.base import BaseCommand
from model_training.CB_Filtration import CB_Filtration
from homepage.models import Ratings

class Command(BaseCommand):

    def handle(self, *args, **options):
        print(type(Ratings.objects.order_by('-score')[0]))
        # cbf = CB_Filtration(min_sim=0.1)
        # cbf.load_data()
        # # cbf.calc_similarity()
        # # cbf.save_similarities_with_postgre()