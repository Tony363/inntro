# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, NameForm, ContactForm,ToDo
from .models import TodoList
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect,csrf_exempt


# @login_required
def home(request):
    inital_data = {
        'title':"My awesome title",
        'content':'insert some content',
        "Text":'some side notes here',
    }
    tasks = TodoList.objects.all()
    if request.method == 'POST':
        form = ToDo(request.POST or None, instance=tasks)
        # List = TodoList.objects.ordered_by('id')

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            return HttpResponse(f'{title}:{content}',content_type="text/plain")
            # return redirect('/')

    else:
        form = ToDo(initial=inital_data)
   
    return render(request, 'admin/events/home.html/',{'tasks':tasks,'form':form})#'ToDoList':TodoList

def Signup(request):
        
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
            #return new URL
            form.save()
            your_name = form.cleaned_data['your_name']
            print(your_name)
            # return HttpResponseRedirect('/thanks/')
            return HttpResponse('{}'.format(your_name))
           
    #if a GET(or any other method) we'll create a blannk form        
    else:
        form = NameForm()
        # return HttpResponse('{}'.format(NameForm))
    return render(request,'simple_form.html',{'form':form})

@csrf_exempt
def your_name(request):
    return HttpResponse('thanks',content_type="text/plain")

def mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            print(subject,message,sender)
            if cc_myself:
                recipients.append(sender)
                 
            # send_mail(subject, message, sender,recipients)
            return HttpResponse('/thanks/')
    else:
        form = ContactForm()
       
    return render(request,'contact_forms.html',{'form':form})



    
  