# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect

# Create your views here.

# def Hello_World(requests):
#     template = loader.get_template('admin/events/change_list.html')
#     context = {
#         'previous_month':previous_month,
#         'next_month': next_month,
#     }
#     return HttpResponse(template.render(context,requests))

# @login_required
def home(request):
    return render(request, 'admin/events/home.html')

def register(request):
    if request.method == 'GET':
        form = SignUpForm(request.GET)
        return render(request,'admin/events/signup.html',{'form':form})
        
    if request.method == 'POST':
        form = SignUpForm()
       
        if form.is_valid():
            form.save()
        return redirect('home')
        # else:
        #     return redirect('register')
            # form = SignUpForm()
        # return render(request,'admin/events/signup.html',{'form':form})
    
  