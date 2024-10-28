from django.core.management.base import BaseCommand
from model_training.FWLS import *

class Command(BaseCommand):

    def handle(self, *args, **options):    
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
        logger = logging.getLogger('funkSVD')
        logger.info("[BEGIN] Calculating Feature Weighted Linear Stacking...")

        fwls = FWLSCalculator(save_path="recsys/ml_models", data_size=10000)
        fwls.get_real_training_data()
        logger.info(fwls.train_data)

        fwls.calculate_predictions_for_training_data()
        fwls.calculate_feature_functions_for_training_data()
        logger.info("Freatures trained")
        logger.info("[BEGIN] training of FWLS")
        fwls.train()
        logger.info("[END] training of FWLS")
        logger.info("[END] Calculating Feature Weighted Linear Stacking...")

        