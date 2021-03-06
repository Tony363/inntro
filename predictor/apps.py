# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

import xgboost as xgb
import os
import pickle


class EventsConfig(AppConfig):
    name = 'events'

class PredictorConfig(AppConfig):

    # create path to models
    path = os.path.join(settings.MODELS,'xgbregression.model')

    # load models into separate variables
    # these will be accessible via this class 
    loaded_models = xgb.Booster()
    loaded_models.load_model(path)


    

    