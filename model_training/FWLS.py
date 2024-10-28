import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prs_project.settings")

import django

django.setup()

import pickle
import logging

import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from homepage.models import MLRatings
from recsys.rec_models.CB import ContentBasedRecommender
from recsys.rec_models.CF import CollaborativeRecommender
from recsys.rec_models.Hybrid import FeatureWeightedLinearStacking


def ensure_dir(file_path):
    
    directory = os.path.dirname(os.getcwd() + file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


class FWLSCalculator(object):
    def __init__(self, save_path, data_size=1000):
        self.save_path = save_path
        self.logger = logging.getLogger('FWLS')
        self.train_data = None
        self.test_data = None
        self.rating_count = None
        self.cb = ContentBasedRecommender()
        self.cf = CollaborativeRecommender()
        self.fwls = FeatureWeightedLinearStacking()
        self.data_size = data_size

    def get_real_training_data(self):
        columns = ['movie', 'user', 'score']
        ratings_data = MLRatings.objects.all().values(*columns)[:self.data_size]
        df = pd.DataFrame.from_records(ratings_data, columns=columns)
        self.train_data, self.test_data = train_test_split(df, test_size=0.2)
        self.logger.debug("training data loaded {}".format(len(df)))

    def calculate_predictions_for_training_data(self):
        self.logger.debug("[BEGIN] getting predictions")

        self.train_data['cb'] = self.train_data.apply(lambda data:
                                                      self.cb.predict_score(data['user'],
                                                                            data['movie'], train=True), axis=1)

        self.train_data['cf'] = self.train_data.apply(lambda data:
                                                      self.cf.predict_score(data['user'],
                                                                            data['movie'], train=True), axis=1)

        print(self.train_data)
        self.logger.debug("[END] getting predictions")
        return None

    def calculate_feature_functions_for_training_data(self):
        self.logger.debug("[BEGIN] calculating functions")
        self.train_data['cb1'] = self.train_data.apply(lambda data:
                                                       data['cb'] * self.fwls.fun1(), axis=1)
        self.train_data['cb2'] = self.train_data.apply(lambda data:
                                                       data['cb'] * self.fwls.fun2(data['user']), axis=1)

        self.train_data['cf1'] = self.train_data.apply(lambda data:
                                                       data['cf'] * self.fwls.fun1(), axis=1)
        self.train_data['cf2'] = self.train_data.apply(lambda data:
                                                       data['cf'] * self.fwls.fun2(data['user']), axis=1)


        self.logger.debug("[END] calculating functions")
        return None

    def build(self, train_data=None, params=None):

        if params:
            self.save_path = params['save_path']
            self.data_size = params['data_sample']

        if train_data is not None:
            self.train_data = train_data
            if self.data_size > 0:
                self.train_data = self.train_data.sample(self.data_size)
                self.logger.debug("training sample of size {}".format(self.train_data.shape[0]))
        else:
            self.get_real_training_data()

        self.calculate_predictions_for_training_data()
        self.calculate_feature_functions_for_training_data()

        return self.train()

    def train(self, ratings=None, train_feature_recs=False):

        regr = linear_model.LinearRegression(fit_intercept=True,
                                             n_jobs=-1,
                                             normalize=True)

        regr.fit(self.train_data[['cb1', 'cb2', 'cf1', 'cf2']], self.train_data['score'])
        self.logger.info(regr.coef_)

        predictions = regr.predict(self.train_data[['cb1', 'cb2', 'cf1', 'cf2']])
        mse = mean_squared_error(self.train_data['score'], predictions)
        self.logger.info(f'MSE: {mse**0.5}')

        result = {'cb1': regr.coef_[0],
                  'cb2': regr.coef_[1],
                  'cf1': regr.coef_[2],
                  'cf2': regr.coef_[3],
                #   'intercept': regr.intercept_[4]
                }
        self.logger.debug(result)
        self.logger.debug(len(self.train_data))
        self.logger.debug(self.train_data.iloc[100])
        ensure_dir(self.save_path)
        with open(self.save_path + 'fwls_parameters.data', 'wb') as ub_file:
            pickle.dump(result, ub_file)
        return result