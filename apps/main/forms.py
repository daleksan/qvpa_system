# -*- coding: utf-8 -*-
from django import forms
# from .models import User, Game, Participants   # fill in custom user info then save it
# from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя', max_length=64)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
