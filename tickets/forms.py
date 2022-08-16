from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import OffererProfile


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, user_group):
        user = super().save()
        user.groups.add(user_group)
        return user


class OffererProfileForm(forms.ModelForm):
    class Meta:
        model = OffererProfile
        fields = ("address", "phone")

    def save(self, user):
        profile = super().save(commit=False)
        profile.user = user
        profile.save()
        return profile
