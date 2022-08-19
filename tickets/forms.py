from django import forms
from django.contrib.auth.forms import UserCreationForm
from betterforms.multiform import MultiModelForm

from models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

class OffererForm(forms.ModelForm):
    class Meta:
        model = Offerer
        exclude = ["user"]


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        exclude = ["user"]


class OffererSignUpForm(MultiModelForm):
    form_classes = {"user": UserCreationForm, "profile": ProfileForm}

    def save(self, commit=True):
        objects = super(OffererSignUpForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            profile = objects['profile']
            profile.user = user
            profile.save()

        return objects

class BuyerSignUpForm(MultiModelForm):
    form_classes = {"user": UserCreationForm, "buyer": BuyerForm}

    def save(self, commit=True):
        objects = super(BuyerSignUpForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            profile = objects['profile']
            profile.user = user
            profile.save()

        return objects
