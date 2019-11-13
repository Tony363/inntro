# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect,render

# Create your views here.

# def Hello_World(requests):
#     template = loader.get_template('admin/events/change_list.html')
#     context = {
#         'previous_month':previous_month,
#         'next_month': next_month,
#     }
#     return HttpResponse(template.render(context,requests))

@login_required
def home(request):
    return render(request, 'events/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
        return render(request,'events/signup.html',{'form':form})
    
  