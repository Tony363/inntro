# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, NameForm, ContactForm
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail


# @login_required
def home(request):
    return render(request, 'admin/events/home.html/')

def Signup(request):
    # if request.method == 'GET':
    #     form = SignUpForm(request.GET)
    #     return render(request,'admin/events/signup.html',{'form':form})
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
       
        if form.is_valid():
          
            print(form.cleaned_data['email'])
            print(form.cleaned_data['first_name'])
            print(form.cleaned_data['last_name'])
            form.save()
            return render(request, 'admin/events/login.html')
    else:
        form = SignUpForm()
    return render(request,'signup.html', {'form':form})

def get_name(request):
    #if request is POST
    if request.method == 'POST':
        #populate instance of form with POST data
        form = NameForm(request.POST)
        #check if instance POST data is valid
        if form.is_valid():
            #reutrn new URL
            form.save()
            return HttpResponse('at least i got it to work')
    #if a GET(or any other method) we'll create a blannk form        
    else:
        form = NameForm()
    return render(request,'simple_form.html',{'form':form})

def mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)
            
            send_mail(subject, message, sender,recipients)
            return HttpResponseRedirect('/thanks/')



    
  