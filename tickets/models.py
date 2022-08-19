from django.db import models
from django.contrib.auth.models import User

from .validators import cep_validator, phone_validator
from .user_extension import is_buyer, is_offerer, is_regulator

User.add_to_class("is_buyer", is_buyer)
User.add_to_class("is_offerer", is_offerer)
User.add_to_class("is_regulator", is_regulator)


class Address(models.Model):
    cep = models.CharField(max_length=9, validators=[cep_validator])
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)


class Buyer(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)


class Offerer(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)


class Regulator(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    picture = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    def approve_offerer(self):
        if self.is_offerer:
            self.is_offerer_aproved = True
            self.save()
        else:
            raise Exception("User is not an offerer")
