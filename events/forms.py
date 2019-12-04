from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='')
    first_name = forms.CharField(max_length=30, required=False, help_text="")
    last_name = forms.CharField(max_length=30, required=False, help_text="")


    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1','password2')

    def save(self,commit=True):
        user = super(SignUpForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user