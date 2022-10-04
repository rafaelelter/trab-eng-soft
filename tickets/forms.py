import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import HiddenInput, PasswordInput
from django.core.exceptions import ValidationError

from .models import Profile, Address, Ticket, validate_random_id

from datetime import timezone


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        label="E-mail",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuário"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class OffererProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = True
        self.fields["place_name"].required = True

    class Meta:
        model = Profile
        fields = ("place_name", "phone", "picture")
        labels = {
            "place_name": "Nome do estabelecimento",
            "phone": "Telefone",
            "picture": "Foto de perfil",
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "cep",
            "street_name",
            "street_number",
            "neighborhood",
            "city",
            "state",
        )
        labels = {
            "cep": "CEP",
            "street_name": "Nome da rua",
            "street_number": "Número",
            "neighborhood": "Bairro",
            "city": "Cidade",
            "state": "Estado",
        }


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone", "picture")
        labels = {"phone": "Telefone", "picture": "Foto de perfil"}


class SearchOffererForm(forms.Form):
    search = forms.CharField(label="Buscar", max_length=100)


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("description", "price", "picture")
        labels = {
            "description": "Descrição",
            "price": "Preço",
            "picture": "Foto",
        }


class TicketPurchaseForm(forms.ModelForm):
    expiration_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "datepicker",
                "type": "date",
            },
        ),
        required=False,
    )
    expiration_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "class": "timepicker",
                "type": "time",
            },
        ),
        required=False,
    )

    class Meta:
        model = Ticket
        fields = ("password", "expiration_date", "expiration_time")
        labels = {
            "password": "Senha",
            "expiration_date": "Data de expiração",
            "expiration_time": "Hora de expiração",
        }

    def clean_expiration(self):
        expiration_date = self.cleaned_data["expiration_date"]
        expriration_time = self.cleaned_data["expiration_time"]
        expiration = datetime.datetime.combine(expiration_date, expriration_time)
        if expiration < datetime.datetime.now():
            raise ValidationError("Data de expiração inválida")

    def clean(self):
        self.clean_expiration()
        return super().clean()


class TicketValidationForm(forms.Form):
    random_id = forms.CharField(max_length=8, validators=[validate_random_id])
    password = forms.CharField(
        label="Senha", max_length=100, widget=PasswordInput, required=False
    )
