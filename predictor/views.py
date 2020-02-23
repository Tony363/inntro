# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .apps import PredictorConfig
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,request
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import User

from .forms import *
from .models import *

from sklearn.model_selection import train_test_split
from wsgiref.util import FileWrapper

import yfinance as yf 
import pandas as pd 
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import requests, json, os, shap, tempfile, zipfile, mimetypes


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
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                form.save()
                
                request.session['stock'] = stock
                request.session['start'] = start_date
                request.session['end'] = end_date

                requested_stock = yf.Ticker(str(stock))
                print(requested_stock.info)
                
            except Exception:
               return render(request,'predictions.html')
            
            return redirect('visualization')
       
    else:
        form = Index_form()

        return render(request,'predictions.html',{'form':form})


def logout(request):
    return render(request,'registration/logout.html')

def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            reg_username = form.cleaned_data['reg_username']
            reg_email = form.cleaned_data['reg_email']
            reg_password = form.cleaned_data['reg_password']
            return HttpResponse('thats it for now')
    else:
        form = register_form()
    return render(request,'registration/register.html')



def visualization(request):
    path = os.path.join(settings.MODELS,'xgbregression.model')

    if request.method == 'GET':
        
        stock_db = Index.objects.all().last()
        stock = request.session['stock']
        start = request.session['start']
        end = request.session['end']
        
        requested_stock = yf.Ticker(str(stock))

        history = requested_stock.history(start=str(start), end=str(end))
        stock = pd.DataFrame(history)
        stock.to_csv(staticfiles_storage.path('numpy_array/stock.csv'))

        stock_changes = stock.pct_change()
        stock_changes.drop(stock_changes.index[0],inplace=True)
        stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
        stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
        stock_matrix.columns = [ f'Days_{i+1}'for i in range(len(stock_matrix.columns))]
        
        X = stock_matrix.loc[:,'Days_2':]
        y = stock_matrix['Days_1']

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4)

        X_train.to_csv(staticfiles_storage.path('numpy_array/X_train.csv'))
        X_test.to_csv(staticfiles_storage.path('numpy_array/X_test.csv'))
        y_train.to_csv(staticfiles_storage.path('numpy_array/y_train.csv'))
        y_test.to_csv(staticfiles_storage.path('numpy_array/y_test.csv'))    
        
        dtrain = xgb.DMatrix(X_train,y_train)
        dtest = xgb.DMatrix(X_test,y_test)

        loaded_models = xgb.Booster()
        loaded_models.load_model(path)
        prediction = loaded_models.predict(dtest)
        np.savetxt(staticfiles_storage.path('numpy_array/prediction.csv'),prediction,delimiter=',')

        explainer = shap.TreeExplainer(loaded_models)
        shap_values_XGB_test = explainer.shap_values(X_test)
        shap_values_XGB_train = explainer.shap_values(X_train)

        df_shap_XGB_test = pd.DataFrame(shap_values_XGB_test,columns=X_test.columns.values)
        df_shap_XGB_train = pd.DataFrame(shap_values_XGB_train,columns=X_train.columns.values)

        shap.initjs()

        shap.force_plot(explainer.expected_value,shap_values_XGB_test[0],X_test.iloc[[0]],show=False,matplotlib=True).savefig(staticfiles_storage.path('image/initial.png'))
        # shap.force_plot(explainer.expected_value,shap_values_XGB_test,X_test).savefig('/home/tony/Desktop/My_repos/inntro/predictor/static/image/initial.png')
       
        shap.save_html(staticfiles_storage.path('image/wave_plot.png'),shap.force_plot(explainer.expected_value,shap_values_XGB_test,X_test,show=False))

        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train,plot_type='bar',show=False)
        s_plot.savefig(staticfiles_storage.path('image/barplot.png'))
       
        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train,show=False)
        s_plot.savefig(staticfiles_storage.path('image/shap_value.png'))
     
        # shap.dependence_plot('Days_2',shap_values_XGB_train,X_train).savefig('/home/tony/Desktop/github_repos/inntro/predictor/static/image/scatter.png')

        return render(request,'images.html')
    else:
        return render(request,'images.html')

def X_train(request):
    csv = staticfiles_storage.path('numpy_array/X_train.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('X_train.csv')
        return response

    return HttpResponse('what do you want to download again?')

def X_test(request):
    csv = staticfiles_storage.path('numpy_array/X_test.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('X_test.csv')
        return response

    return HttpResponse('what do you want to download again?')

def y_train(request):
    csv = staticfiles_storage.path('numpy_array/y_train.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('y_train.csv')
        return response

    return HttpResponse('what do you want to download again?')

def y_test(request):
    csv = staticfiles_storage.path('numpy_array/y_test.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('y_test.csv')
        return response

    return HttpResponse('what do you want to download again?')

def stock(request):
    csv = staticfiles_storage.path('numpy_array/stock.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('stock.csv')
        return response

    return HttpResponse('what do you want to download again?')
    
def prediction(request):
    csv = staticfiles_storage.path('numpy_array/prediction.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == 'POST':
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('prediction.csv')
        return response

    return HttpResponse('what do you want to download again?')

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