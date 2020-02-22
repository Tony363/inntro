from django import forms
from .models import *


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
        model = Download
        fields = ['csv']
    
    def save(self,commit=True):
        user = super(download_form,self).save(commit=False)
        user.csv = self.cleaned_data['csv']
