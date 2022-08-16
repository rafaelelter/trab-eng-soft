from django.db import models
from django.core.validators import RegexValidator

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

    def __str__(self):
        return self.user.username
