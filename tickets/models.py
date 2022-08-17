from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

# Create your models here.
class OffererProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(r"^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$")
        ],
        help_text="(99) 99999-9999",
        error_messages={"invalid": "Formato de telefone inválido."},
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("offerer-detail", kwargs={"pk": self.pk})


class Ticket(models.Model):
    offerer = models.ForeignKey(OffererProfile, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="tickets/images/", blank=True)
    buyer = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, blank=True, null=True
    )
    password = models.CharField(max_length=20, blank=True)
    validated = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("ticket-detail", kwargs={"pk": self.pk})
