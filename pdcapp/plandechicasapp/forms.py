# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from plandechicasapp.models import UserProfile, Pot

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form_element','placeholder':'Username'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form_element','placeholder':'email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form_element','placeholder':'Password'}), required=True)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form_element','placeholder':'firstname'}), required=True)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form_element','placeholder':'lastname'}), required=True)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form_element','placeholder':'Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form_element','placeholder':'Password'}), required=True)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'friends')

class WhatForForm(forms.ModelForm):
    class Meta:
        model = Pot
        exclude = ('owner', 'user_list', 'price', 'product_list', 'is_paid', 'is_purchased')
        widgets = {
            'date': SelectDateWidget(),
        }

class WhoForm(forms.ModelForm):
    class Meta:
        model = Pot
        exclude = ('owner', 'what_for', 'who_for' , 'date','price', 'product_list', 'is_paid', 'is_purchased')
        widgets = {
            'user_list': CheckboxSelectMultiple()
        }