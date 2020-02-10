# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .apps import PredictorConfig
from django.http import HttpResponse,JsonResponse,request
from rest_framework.views import APIView
from django.conf import settings

from .forms import Index_form
from .models import Index

from sklearn.model_selection import train_test_split
import yfinance as yf 
import pandas as pd 
import numpy as np
import xgboost as xgb
import requests
import json 
import os

Alpaca_API_key = 'PKLQHCF2P3VRXDC4LBBW'

Alpaca_secret_key = 'vBJbM3zLE42EQQ3xX0MXTajddGOyUU6Hd4b7zw0m'

Endpoint_url = 'https://paper-api.alpaca.markets'

Account_url = f'{Endpoint_url}/v2/account'

Order_url = f'{Endpoint_url}/v2/orders'

Headers = {'APCA-API-KEY-ID':Alpaca_API_key,'APCA-API-SECRET-KEY':Alpaca_secret_key}

r = requests.get(Account_url,headers=Headers)

dic_r = json.loads(r.content)

def Index(request):
    path = os.path.join(settings.MODELS,'xgbregression.model')
    initial_value = {
        'stock','Entire stock'
    }
    if request.method == 'POST':
        form = Index_form(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            requested_stock = yf.Ticker(stock)
            history = requested_stock.history(period='max')
            stock = pd.DataFrame(history)
            stock_changes = stock.pct_change()
            stock_changes.drop(stock_changes.index[0],inplace=True)
            stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
            stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
            stock_matrix.columns = [ f'Day {i+1}'for i in range(len(stock_matrix.columns))]
            # print(stock_matrix)
            X = np.asarray(stock_matrix.loc[:,'Day 2':])
            y = np.asarray(stock_matrix['Day 1'])
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
            dtrain = xgb.DMatrix(X_train,y_train)
            dtest = xgb.DMatrix(X_test,y_test)
            loaded_models = xgb.Booster()
            loaded_models.load_model(path)
            prediction = loaded_models.predict(dtest)
            prediction = np.asarray(prediction)
            print(prediction)
            return render(request,'results.html',{'prediction':prediction})
    else:
        form = Index_form()
    return render(request,'predictions.html',{'form':form})


# Create your views here.
def Alpaca_order_manager(request,symbol,qty,side,tpe,time_in_force):
    data = {
        'symbol':symbol,
        'qty':qty,
        'side':side,
        'type':tpe,
        'time_in_force':time_in_force
    }
    r = requests.post(Order_url,json=data,headers=Headers)
    return json.loads(r.content)

class call_model(APIView):
    def get(self,request):
        if request.method == 'GET':

           
            

            # predict stock d test data
            prediction = PredictorConfig.predict(stock)

            return HttpResponse(prediction)