from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class login_form(forms.ModelForm):

    class Meta():
        model = login
        fields = ['username','password']
    
    def save(self,commit=True):
        user = super(login_form,self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        if commit:
            user.save()
        return user

class Index_form(forms.ModelForm):
    
    
    class Meta():
        model = Index
        fields = ['stock','start_date','end_date']

    def save(self, commit=True):
        user = super(Index_form, self).save(commit=False)
        user.stock = self.cleaned_data['stock']
        user.start_date = self.cleaned_data['start_date']
        user.end_date = self.cleaned_data['end_date']
        if commit:
            user.save()
        return user

class download_form(forms.ModelForm):

    class Meta():
        model = save_data
        fields = ['csv']
    
    def save(self,commit=True):
        user = super(download_form,self).save(commit=False)
        user.csv = self.cleaned_data['csv']
