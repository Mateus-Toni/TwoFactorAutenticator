import re

CPF_PATTERN = r'([\d]{3}\.?[\d]{3}\-?[\d]{2})'

def validate_data_user(user):

    if re.match(pattern=CPF_PATTERN, string=user.cpf):

        ...