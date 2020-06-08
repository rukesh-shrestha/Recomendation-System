from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Contactus

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2','first_name','last_name']


# class ContactUsForm(forms.ModelForm):
# 	class Meta:
# 		model = Contactus
# 		fields = [
# 			'name',
# 			'emails',
# 			'subjects',
# 			'descriptions'
# 	]


class ContactUsForm(forms.Form):
    # model = Contactus
    name = forms.CharField(max_length=50)
    emails = forms.EmailField(max_length=200)
    subjects = forms.CharField(max_length=100)
    descriptions = forms.CharField(max_length=400)
