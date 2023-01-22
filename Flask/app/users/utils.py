import re

CPF_PATTERN = r'([\d]{3}\.?[\d]{3}\-?[\d]{2})'
EMAIL_PATTERN = r'([A-z\.\_\-\d]+@[A-z]+\.com.?b?r?)'

def validate_data_user(user):

    if not re.match(pattern=CPF_PATTERN, string=user.cpf):

        return False

    elif not re.match(pattern=EMAIL_PATTERN, string=user.email):

        return False

    else:

        return True
    
    
def cpf_autenticator(cpf): # refactor

    mult = 10
    sum_cpf = 0
    last_num = ''

    for run in range(2, 0, -1):

        for number in cpf[:-run]:

            sum_cpf += int(number) * mult

            mult -= 1

        mult = 11

        last_num += str(mult - (sum_cpf % mult))

        sum_cpf = 0

    if last_num == cpf[-2:]:

        return True

    return False

