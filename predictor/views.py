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
from django.contrib.auth.decorators import login_required
from django_pandas.io import read_frame

from .forms import *
from .models import *

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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



@login_required
def home(request):   
    if request.method == 'POST':
        form = Index_form(request.POST)

        if form.is_valid():    
            # try:
            stock = form.cleaned_data['stock']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            form.save()
            
            request.session['stock'] = stock
            request.session['start'] = start_date
            request.session['end'] = end_date

            requested_stock = yf.Ticker(str(stock))              
            history = requested_stock.history(start=start_date, end=end_date)
        
            history.reset_index(inplace=True)
            history.index.name = 'ID'
            history.columns = ['Date','Open','High','Low','Close','Volume','Dividends','Stock_splits']

            history.to_sql('DFModel',con=engine,if_exists='replace',index=True,index_label='ID')
            
            stock_changes = history.set_index('Date').pct_change()
            stock_changes.drop(stock_changes.index[0],inplace=True)
            stock_matrix = pd.concat([stock_changes.Close.shift(-i) for i in range(100)],axis=1)
            stock_matrix.drop(stock_matrix.index[-99:],inplace=True)
            stock_matrix.columns = [ f'Days_{i}'for i in range(len(stock_matrix.columns))]
            stock_matrix.reset_index(inplace=True)
            stock_matrix.index.name = 'ID'

            stock_matrix.to_sql('PCT_Change',con=engine,if_exists='replace',index=True,index_label='ID')
                
            # except Exception as e:
            #     print(e)
            #     return render(request,'home.html',{'form':form})
       
            return render(request,'PctMatrix.html')
       
    else:
        form = Index_form()
        return render(request,'home.html',{'form':form})


def logout(request):
    return render(request,'registration/logout.html')

def data(request):
    return render(request,'data.html')

def to_split_data(request):
    return render(request,'splitting.html')


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
    static = os.listdir(os.path.join(settings.STATIC_ROOT,'image/')) 
    path = os.path.join(settings.MODELS,'xgbregression.model')

    X_train = read_frame(Xtrain.objects.all()).drop(columns='ID')
    X_test = read_frame(Xtest.objects.all()).drop(columns='ID')
    y_train = read_frame(Ytrain.objects.all()).drop(columns='ID')
    y_test = read_frame(Ytest.objects.all()).drop(columns='ID')

    
    
    dtrain = xgb.DMatrix(X_train,y_train,nthread=-1)
    dtest = xgb.DMatrix(X_test,y_test,nthread=-1)

    if request.method == 'GET':
        
        loaded_models = xgb.Booster()
        loaded_models.load_model(path)
        
        xgb.plot_importance(loaded_models,max_num_features=10)
        fig = plt.gcf()
        
        fig.savefig(staticfiles_storage.path('image/importance.png'))
    
        xgb.plot_tree(loaded_models)
        fig = plt.gcf()
      
        fig.savefig(staticfiles_storage.path('image/tree.png'))
  
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

        
        shap.dependence_plot('Days_1',shap_values_XGB_train,X_train,show=False)
        fig = plt.gcf()
        fig.savefig(staticfiles_storage.path('image/dependance.png'))

        return render(request,'images.html',{'image':static, 'tony':static})
    else:
        return render(request,'images.html')




def to_PctMatrix(request):
    csv = staticfiles_storage.path('numpy_array/PctMatrix.csv')
    content_type = mimetypes.guess_type(csv)[0]

    if request.method == "POST":
        wrapper = FileWrapper(open(csv))
        response = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = os.path.getsize(csv)
        response['Content-Disposition'] = "attachment; filename={}".format('PctMatrix.csv')
        return response
        
    return HttpResponse('that\'s the PctMatrix')



def split_data(request):
    csv = staticfiles_storage.path('numpy_array/PctMatrix.csv')
    content_type = mimetypes.guess_type(csv)[0]
    pct_matrix = PCT_Change.objects.all()
  
    if request.method == 'GET':
        df = read_frame(pct_matrix)
        
        X = df.loc[:,'Days_1':]
        y = df['Days_0']

        X_train = df.loc[:round(df.shape[1]*0.8),'Days_1':]
        X_test = df.loc[round(df.shape[1]*0.8):,'Days_1':]
        y_train = df.loc[:round(df.shape[1]*0.8),'Days_0']
        y_test = df.loc[round(df.shape[1]*0.8):,'Days_0']

     
        X_train.to_sql('Xtrain',con=engine,if_exists='replace',index=True,index_label='ID')
        X_test.to_sql('Xtest',con=engine,if_exists='replace',index=True,index_label='ID')
        y_train.to_sql('Ytrain',con=engine,if_exists='replace',index=True,index_label='ID')
        y_test.to_sql('Ytest',con=engine,if_exists='replace',index=True,index_label='ID')
     
    
        return render(request,'splitted.html')
    return HttpResponse('fail')  

def predict(request):

    path = os.path.join(settings.MODELS,'xgbregression.model')  

    if request.method == "POST":
        X_train = read_frame(Xtrain.objects.all())
        X_test = read_frame(Xtest.objects.all())
        y_train = read_frame(Ytrain.objects.all())
        y_test = read_frame(Ytest.objects.all())
       
        
        dtrain = xgb.DMatrix(X_train,y_train.drop(columns='ID'),nthread=-1)
        dtest = xgb.DMatrix(X_test,y_test.drop(columns='ID'),nthread=-1)

        loaded_models = xgb.Booster()
        loaded_models.load_model(path)

        # print(loaded_models.eval(dtest,name='eval'))
        # print(loaded_models.eval_set([(dtest,"Test")]))
        # print(loaded_models.eval(dtrain,name='eval'))
        # print(loaded_models.eval_set([(dtrain,'Train')]))

        prediction = loaded_models.predict(dtest,pred_leaf=True)
        # print(prediction)

        # accuracy = mean_squared_error(prediction,y_test)

        np.savetxt(staticfiles_storage.path('numpy_array/prediction.csv'),prediction,delimiter=',')
        return render(request,'MVND.html')#{'accuracy':accuracy})
    return HttpResponse('predicting')

def MVND(request):
    csv = staticfiles_storage.path('numpy_array/prediction.csv')
    content_type = mimetypes.guess_type(csv)[0]
    testleaf = genfromtxt('{}'.format(csv),delimiter=',')
    
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
    # print(multivariate_normal_distribution)
    wrapper = FileWrapper(open(staticfiles_storage.path('numpy_array/multivariate_normal_distribution.csv')))
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(staticfiles_storage.path('numpy_array/multivariate_normal_distribution.csv'))
    response['Content-Disposition'] = "attachment; filename={}".format('MVND.csv')
    
    return response



def X_train(request): 
    
    q = Xtrain.objects.all()
    df = read_frame(q)
    df.to_csv(staticfiles_storage.path('numpy_array/X_train.csv'))
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

    q = Xtest.objects.all()
    df = read_frame(q)
    df.to_csv(staticfiles_storage.path('numpy_array/X_test.csv'))
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
    
    q = Ytrain.objects.all()
    df = read_frame(q)
    df.to_csv(staticfiles_storage.path('numpy_array/y_train.csv'))
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

    q = Ytest.objects.all()
    df = read_frame(q)
    df.to_csv(staticfiles_storage.path('numpy_array/y_test.csv'))
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
    
    q = DFModel.objects.all()
    df = read_frame(q)
    df.to_csv(staticfiles_storage.path('numpy_array/stock.csv'))
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
    pred = read_frame(Pred.objects.all()).drop(columns='ID')

    if request.method == 'POST':
        pred.to_csv(csv)
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