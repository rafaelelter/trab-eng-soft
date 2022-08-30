from django.db import models

from .validators import cep_validator, phone_validator, is_offerer, is_regulator


class Address(models.Model):
    cep = models.CharField(max_length=9, validators=[cep_validator])
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)


class OffererApproval(models.Model):
    approved_offerer = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="approved_offerer",
        validators=[is_offerer],
        unique=True,
    )
    approved_by = models.OneToOneField(
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
    picture = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    def is_approved(self):
        if self.user_type == "O":
            return hasattr(self.user, "approved_offerer")
        raise NotImplementedError("Only offerers can be approved")
