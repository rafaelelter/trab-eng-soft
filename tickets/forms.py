from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import OffererProfile, Ticket


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

class OffererSearchForm(forms.Form):
    search = forms.CharField(max_length=100)
    def __init__(self, *args, **kwargs):
        super(OffererSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'form-control'})

class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("description", "price", "image")
