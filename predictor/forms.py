from django import forms
from .models import *
from django.contrib.auth.models import User


# class register_form(forms.ModelForm):
#     username = forms.CharField(max_length=100)
#     email = forms.CharField(max_length=100)
#     password = forms.CharField(max_length=100)

#     user = User.objects.create_user(username,email,password)
#     user.save()


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
