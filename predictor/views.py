# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .apps import PredictorConfig
from django.http import HttpResponse,JsonResponse,request
from rest_framework.views import APIView

import yfinance as yf 
import pandas as pd 
import numpy as np
import xgboost as xgb
import requests
import json 

Alpaca_API_key = 'PKLQHCF2P3VRXDC4LBBW'

Alpaca_secret_key = 'vBJbM3zLE42EQQ3xX0MXTajddGOyUU6Hd4b7zw0m'

Endpoint_url = 'https://paper-api.alpaca.markets'

Account_url = f'{Endpoint_url}/v2/account'

Order_url = f'{Endpoint_url}/v2/orders'

Headers = {'APCA-API-KEY-ID':Alpaca_API_key,'APCA-API-SECRET-KEY':Alpaca_secret_key}

r = requests.get(Account_url,headers=Headers)

dic_r = json.loads(r.content)

def Index(request):
    Initial_value = {
        
    }
    if request.method == 'POST':
        form = form.Index(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            return render(request,'result.html',stock=stock)
    else:
        form = form.Index()
    return render(request,'predictions.html')

def yahoo_finance_history(request):
    if request.method == 'GET':
        requested_stock = yf.Ticker('TSLA')
        history = requested_stock.history(period='max')
        stock = pd.DataFrame(history)
        stock_changes = stock.pct_change()
        stock_changes.drop(stock_changes.index[0],inplace=True)
        stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
        stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
        stock_matrix.columns = [ f'Day {i+1}'for i in range(len(stock_matrix.columns))]
        return HttpResponse(np.asarray(stock_matrix))

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

            #get stock name from request
            stock = request.GET.get('stock')

            # predict stock d test data
            prediction = PredictorConfig.predict(stock)

            return HttpResponse(prediction)