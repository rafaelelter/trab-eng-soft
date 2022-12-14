from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .badwords import BAD_WORDS

from datetime import timezone

cep_validator = RegexValidator(
    regex=r"^\d{5}-\d{3}$", message="CEP inválido. Exemplo: 12345-678"
)
phone_validator = RegexValidator(
    regex=r"^\d{2} \d{4,5}-\d{4}$", message="Telefone inválido. Formato: 99 99999-9999"
)


def is_buyer(self):
    return self.profile.user_type == "B"


def is_offerer(self):
    return self.profile.user_type == "O"


def is_regulator(self):
    return self.profile.user_type == "R"


def description_validator(description):
    for word in description.split():
        if word.lower() in BAD_WORDS:
            raise ValidationError("Conteúdo impróprio na descrição do ticket!")
