from django.db import models
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

import sys
from io import BytesIO
from PIL import Image

from .validators import cep_validator, phone_validator, is_offerer, is_regulator


class Address(models.Model):
    cep = models.CharField(max_length=9, validators=[cep_validator])
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.street_name}, {self.street_number}, {self.neighborhood}, {self.city}, {self.state}"


class OffererApproval(models.Model):
    approved_offerer = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="approved_offerer",
        validators=[is_offerer],
        unique=True,
    )
    approved_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="approved_by",
        validators=[is_regulator],
    )
    ts = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=1,
        choices=[
            ("B", "Buyer"),
            ("O", "Offerer"),
            ("R", "Regulator"),
        ],
        default="B",
    )
    place_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    picture = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    def is_approved_offerer(self):
        if self.is_offerer():
            return hasattr(self.user, "approved_offerer")
        return False

    def is_offerer(self):
        return self.user_type == "O"

    def is_buyer(self):
        return self.user_type == "B"

    def is_regulator(self):
        return self.user_type == "R"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    def list_tickets(self):
        if self.is_buyer():
            return self.purchases.all()
        elif self.is_offerer():
            return self.offers.all()
        raise NotImplementedError("Only buyers and offerers can list tickets")


class Ticket(models.Model):
    offerer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="offers")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(default="default_ticket.png", upload_to="ticket_pics", blank=True)
    buyer = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name="purchases", null=True, blank=True
    )
    password = models.CharField(max_length=100, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)
    validated = models.BooleanField(default=False)
    ts = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.description} - {self.price}"
    
    def get_absolute_url(self):
        return reverse("ticket", kwargs={"pk": self.pk})

    def save(self):
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)

    def set_picture_default(self):
        self.picture.delete(save=False)  # delete old image file
        self.picture = 'default_ticket.png' # set default image
        self.save()

    def is_available(self):
        return not self.buyer