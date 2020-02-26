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
from numpy import genfromtxt

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
                print(requested_stock)
                history = requested_stock.history(start=start_date, end=end_date)
                
                stock = pd.DataFrame(history)
                stock.to_csv(staticfiles_storage.path('numpy_array/stock.csv'))
                        
            except Exception:
               return render(request,'home.html',{'form':form})
            # return redirect('visualization')
            return render(request,'PctMatrix.html')
       
    else:
        form = Index_form()

        return render(request,'home.html',{'form':form})


def logout(request):
    return render(request,'registration/logout.html')

def data(request):
    return render(request,'data.html')



def calculations(request):
    testleaf = genfromtxt(staticfiles_storage.path('numpy_array/prediction.csv'),delimiter=',')
    
    tree_pandas = []
    tree_numpy = []
    for column in range(max([len(x) for x in testleaf])):
        
        tree = []
        for row in testleaf[:,column]:
            lst = [0] * int(testleaf[:,column].max())
            try:
                lst[int(row-1)] = 1
                tree.append(lst)
            except IndexError:
                pass
        stats = np.asarray(tree)
        tree_numpy.append(stats)
        df = pd.DataFrame(tree)
        df.columns = ['T{}L{}'.format(column+1,i+1) for i in df.columns]
        df = df.loc[:, (df != 0).any(axis=0)]
        tree_pandas.append(df)
    
    multivariate_normal_distribution = pd.concat(tree_pandas,axis=1)
    multivariate_normal_distribution.to_csv(staticfiles_storage.path('numpy_array/multivariate_normal_distribution.csv'))
    
    return render(request,'calculations.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = RegisterForm()

    return render(request,'registration/register.html',{'form':form})


def visualization(request):
    path = os.path.join(settings.MODELS,'xgbregression.model')

    static = os.listdir(os.path.join(settings.STATIC_ROOT,'image/')) 

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
        stock_matrix.columns = [ f'Days_{i}'for i in range(len(stock_matrix.columns))]
        
        X = stock_matrix.loc[:,'Days_1':]
        y = stock_matrix['Days_0']

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4)

        X_train.to_csv(staticfiles_storage.path('numpy_array/X_train.csv'))
        X_test.to_csv(staticfiles_storage.path('numpy_array/X_test.csv'))
        y_train.to_csv(staticfiles_storage.path('numpy_array/y_train.csv'))
        y_test.to_csv(staticfiles_storage.path('numpy_array/y_test.csv'))    
       
        dtrain = xgb.DMatrix(X_train,y_train,nthread=-1)
        dtest = xgb.DMatrix(X_test,y_test,nthread=-1)

        loaded_models = xgb.Booster()
        loaded_models.load_model(path)
        prediction = loaded_models.predict(dtest,pred_leaf=True)
       
        np.savetxt(staticfiles_storage.path('numpy_array/prediction.csv'),prediction,delimiter=',')

        explainer = shap.TreeExplainer(loaded_models)
        shap_values_XGB_test = explainer.shap_values(X_test)
        shap_values_XGB_train = explainer.shap_values(X_train)

        df_shap_XGB_test = pd.DataFrame(shap_values_XGB_test,columns=X_test.columns.values)
        df_shap_XGB_train = pd.DataFrame(shap_values_XGB_train,columns=X_train.columns.values)

        shap.initjs()

        shap.force_plot(explainer.expected_value,shap_values_XGB_test[0],X_test.iloc[[0]],show=False,matplotlib=True).savefig(staticfiles_storage.path('image/initial.png'))
        # shap.force_plot(explainer.expected_value,shap_values_XGB_test,X_test,show=False,matplotlib=False).savefig('/home/tony/Desktop/My_repos/inntro/predictor/static/image/initial.png')
       
        shap.save_html(staticfiles_storage.path('image/wave_plot.png'),shap.force_plot(explainer.expected_value,shap_values_XGB_test,X_test,show=False))

        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train,plot_type='bar',show=False)
        s_plot.savefig(staticfiles_storage.path('image/barplot.png'))
       
        s_plot = plt.figure()
        shap.summary_plot(shap_values_XGB_train,X_train,show=False)
        s_plot.savefig(staticfiles_storage.path('image/shap_value.png'))

        s_plot = plt.figure()
        shap.dependence_plot('Days_1',shap_values_XGB_train,X_train,show=False)
        s_plot.savefig(staticfiles_storage.path('image/dependence.pdf'))

        return render(request,'images.html',{'image':static, 'tony':static})
    else:
        return render(request,'images.html')




def to_PctMatrix(request):
    csv = staticfiles_storage.path('numpy_array/stock.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == "POST":
        stock = pd.read_csv('{}'.format(csv))
        stock.set_index(['Date'],inplace=True)
        stock.apply(pd.to_numeric)
        stock_changes = stock.pct_change()
        
        stock_changes.drop(stock_changes.index[0],inplace=True)
        stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
        stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
        stock_matrix.columns = [ f'Days_{i}'for i in range(len(stock_matrix.columns))]

        stock_matrix.to_csv(staticfiles_storage.path('numpy_array/PctMatrix.csv'))
        print(stock_matrix)
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('PctMatrix.csv')
        return response
        
    return HttpResponse('that\'s the PctMatrix')

def split_data(request):
    csv = staticfiles_storage.path('numpy_array/PctMatrix.csv')
    content_type = mimetypes.guess_type(csv)[0]
    if request.method == 'GET':
        df = pd.read_csv('{}'.format(csv)).set_index(['Date'])
        print(df)
        X = df.loc[:,'Days_1':]
        y = df['Days_0']
       
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4)
        print(X_test)

        X_train.to_csv(staticfiles_storage.path('numpy_array/X_train.csv'))
        X_test.to_csv(staticfiles_storage.path('numpy_array/X_test.csv'))
        y_train.to_csv(staticfiles_storage.path('numpy_array/y_train.csv'))
        y_test.to_csv(staticfiles_storage.path('numpy_array/y_test.csv'))
        return render(request,'splitted.html')
    return HttpResponse('fail')  

def predict(request):
    path = os.path.join(settings.MODELS,'xgbregression.model')
    X_train = staticfiles_storage.path('numpy_array/X_train.csv')
    X_test = staticfiles_storage.path('numpy_array/X_test.csv')
    y_test = staticfiles_storage.path('numpy_array/y_test.csv')
    y_train = staticfiles_storage.path('numpy_array/y_train.csv')
    X_train_content_type = mimetypes.guess_type(X_train)[0]
    X_test_content_type = mimetypes.guess_type(X_test)[0]
    y_train_content_type = mimetypes.guess_type(y_train)[0]
    y_test_content_type = mimetypes.guess_type(y_test)[0]

    if request.method == "POST":
        X_train = pd.read_csv("{}".format(X_train)).set_index(['Date'])
        X_test = pd.read_csv('{}'.format(X_test)).set_index(['Date'])
        y_train = pd.read_csv("{}".format(y_test)).set_index(['Date'])
        y_test = pd.read_csv("{}".format(y_test)).set_index(['Date'])
        
        
        dtrain = xgb.DMatrix(X_train,y_train,nthread=-1)
        dtest = xgb.DMatrix(X_test,y_test,nthread=-1)
        loaded_models = xgb.Booster()
        loaded_models.load_model(path)
        prediction = loaded_models.predict(dtest,pred_leaf=True)
        np.savetxt(staticfiles_storage.path('numpy_array/prediction.csv'),prediction,delimiter=',')
        return HttpResponse('predicted')
    return HttpResponse('predicting')

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