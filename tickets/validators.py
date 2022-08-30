from django.core.validators import RegexValidator

cep_validator = RegexValidator(regex=r'^\d{5}-\d{3}$', message='CEP inválido.')
phone_validator = RegexValidator(regex=r'^\d{2} \d{4,5}-\d{4}$', message='Telefone inválido.')

def is_buyer(self):
    return self.profile.user_type == "B"

def is_offerer(self):
    return self.profile.user_type == "O"

def is_regulator(self):
    return self.profile.user_type == "R"