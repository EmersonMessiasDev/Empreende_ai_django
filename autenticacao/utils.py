import re
from django.contrib import messages
from django.contrib.messages import constants
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string


def password_is_valid(request, password, confirm_password, nome, usuario, email):
    if len(nome.strip())  == 0:
        messages.add_message(request, constants.ERROR, 'Seu nome não pode ficar em branco')
        return False
    
    if len(usuario.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Seu usuario não pode ficar em branco')
        return False

    if len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Seu usuario não pode ficar em branco')
        return False

    if not re.search(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]', email):
        messages.add_message(request, constants.ERROR, 'E-mail Invalido!')
        return False

    # if not re.search(r'[a-zA-Z0-9_-]+@frwk.com.br', email):
    #     messages.add_message(request, constants.ERROR, 'Você precisa ter um email da framework!')
    #     return False

    if len(password.strip()) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    user = Usuario.objects.filter(userName=usuario)
    if user.exists():
        messages.add_message(request, constants.ERROR, 'Usuario já cadastrado!')
        return False
    
    userEmail = Usuario.objects.filter( usuarioEmail=email)
    if userEmail.exists():
        messages.add_message(request, constants.ERROR, 'Email já cadastrado!')
        return False

    return True


def Alterar_senha(request, password, confirm_password):
    if len(password.strip()) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}



def gerar_senha_temporaria(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

