# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .apps import PredictorConfig
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,request
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse

from .forms import Index_form
from .models import Index

from sklearn.model_selection import train_test_split
from numpy import genfromtxt
import yfinance as yf 
import pandas as pd 
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import requests
import json 
import os
import shap

Alpaca_API_key = 'PKLQHCF2P3VRXDC4LBBW'

Alpaca_secret_key = 'vBJbM3zLE42EQQ3xX0MXTajddGOyUU6Hd4b7zw0m'

Endpoint_url = 'https://paper-api.alpaca.markets'

Account_url = f'{Endpoint_url}/v2/account'

Order_url = f'{Endpoint_url}/v2/orders'

Headers = {'APCA-API-KEY-ID':Alpaca_API_key,'APCA-API-SECRET-KEY':Alpaca_secret_key}

r = requests.get(Account_url,headers=Headers)

dic_r = json.loads(r.content)

def home(request):
     
    if request.method == 'POST':
        form = Index_form(request.POST)

        if form.is_valid():
            
            try:
                stock = form.cleaned_data['stock']
                requested_stock = yf.Ticker(str(stock))
                print(requested_stock.info)
                form.save()
            except ValueError:
               return render(request,'predictions.html')
            
            return redirect('visualization')
       
    else:
        form = Index_form()

        return render(request,'predictions.html',{'form':form})



def visualization(request):
    # print("wtf")
    path = os.path.join(settings.MODELS,'xgbregression.model')

    if request.method == 'GET':
        print('wtf')
        stock = Index.objects.all().last()
        
        requested_stock = yf.Ticker(str(stock))


        history = requested_stock.history(period='max')
        stock = pd.DataFrame(history)
        stock_changes = stock.pct_change()
        stock_changes.drop(stock_changes.index[0],inplace=True)
        stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
        stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
        stock_matrix.columns = [ f'Days_{i+1}'for i in range(len(stock_matrix.columns))]
        
        X = stock_matrix.loc[:,'Days_2':]
        y = stock_matrix['Days_1']

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

        X_train.to_csv('/home/tony/Desktop/github_repos/inntro/predictor/static/numpy_array/X_train.csv')
        X_test.to_csv('/home/tony/Desktop/github_repos/inntro/predictor/static/numpy_array/X_test.csv')
        y_train.to_csv('/home/tony/Desktop/github_repos/inntro/predictor/static/numpy_array/y_train.csv')
        y_test.to_csv('/home/tony/Desktop/github_repos/inntro/predictor/static/numpy_array/y_test.csv')

    
        
        dtrain = xgb.DMatrix(X_train,y_train)
        dtest = xgb.DMatrix(X_test,y_test)

        loaded_models = xgb.Booster()
        loaded_models.load_model(path)
        prediction = loaded_models.predict(dtest)
        prediction = np.asarray(prediction)
            

        explainer = shap.TreeExplainer(loaded_models)
        shap_values_XGB_test = explainer.shap_values(X_test)
        shap_values_XGB_train = explainer.shap_values(X_train)

        df_shap_XGB_test = pd.DataFrame(shap_values_XGB_test)
        df_shap_XGB_train = pd.DataFrame(shap_values_XGB_train)

        shap.force_plot(explainer.expected_value,shap_values_XGB_test[0],X_test.iloc[[0]],show=False,matplotlib=True).savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/initial.png')
        # shap.force_plot(explainer.expected_value,shap_values_XGB_test,X_test).savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/wave_plot.png')
        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train,plot_type='bar')
        s_plot.savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/barplot.png')
       
        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train)
        s_plot.savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/shap_value.png')
     
        # shap.dependence_plot('Days_1',shap_values_XGB_train,X_train).savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/scatter.png')
        # print(prediction)

        return render(request,'images.html')
    else:
        return render(request,'images.html')



# Create your views here.
def Alpaca_order_manager(request,symbol,qty,side,tpe,time_in_force):
    print('wtf')
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