from django import forms
from .models import Index


class Index_form(forms.ModelForm):
    
    
    class Meta():
        model = Index
        fields = ['stock']

    def save(self, commit=True):
        user = super(Index_form, self).save(commit=False)
        user.stock = self.cleaned_data['stock']
        if commit:
            user.save()
        return user
