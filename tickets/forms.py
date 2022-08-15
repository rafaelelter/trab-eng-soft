from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreationForm(UserCreationForm):
    group = forms.ChoiceField(
        choices=[("buyer", "Comprador"), ("unapproved_offerer", "Ofertador")]
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, user_group):
        user = super().save()
        user.groups.add(user_group)
        return user
