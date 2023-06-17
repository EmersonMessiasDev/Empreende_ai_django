from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .utils import email_html, password_is_valid, Alterar_senha
from django.contrib.messages import constants
from django.contrib import messages
from hashlib import sha256, sha1
from django.conf import settings
import os
from datetime import timedelta, date
from django.utils import timezone
from autenticacao.utils import *
from PIL import Image
from empreendeAi.models import *


def logar(request):
    return render(request, "empreendeai/login.html")


def cadastrar(request):
    return render(request, "empreendeai/cadastro.html")


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, 'home/login.html')
    elif request.method == "POST":
        nome = request.POST.get('name')
        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')        
        
        print(f'senha`{senha}')
        print(f'confirmar_senha`{confirmar_senha}')

        if not password_is_valid(request, senha, confirmar_senha, nome, usuario, email):
            return redirect('autenticacao:cadastrar')
        
              
        try:
            senha = sha256(senha.encode()).hexdigest()
            
            user = Usuario.objects.create(nomeUsuario = nome,
                                            userName = usuario,
                                            usuarioEmail = email,
                                            senha=senha,
                                            is_active=False)
            user.save()
            token = sha256(f"{nome}{email}".encode()).hexdigest()
            ativacao = Ativacao(token=token, usuario=user)
            ativacao.save()
                
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/email/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=nome, link_ativacao=f"http://qbhliy.conteige.cloud/autenticacao/ativar_conta/{token}")
                
            # print(f"https://defconecta.tech/auth/ativar_conta/{token}")
            messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso, ative sua conta, link enviado para o seu email!')
            return redirect('autenticacao:logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema solicite ajuda ao suporte!')
            return redirect('autenticacao:cadastrar')
        
        
        
        
def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('home:home')
    user = Usuario.objects.get(usuarioEmail = token.usuario.usuarioEmail)
    print(user)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('home:home')




def validar_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()
    usuario = Usuario.objects.filter(usuarioEmail = email).filter(senha = senha)
    ativado = usuario.filter(is_active = False)
    

    if len(usuario) == 0:
        messages.add_message(request, constants.ERROR, 'Email ou senha invalidos!')
        return redirect('autenticacao:logar')

    elif len(ativado) > 0:
        messages.add_message(request, constants.SUCCESS, 'Ative sua conta antes de logar!')
        return redirect('autenticacao:logar')

    
            
    messages.add_message(request, constants.SUCCESS, 'Usuario logado com sucesso!')
    request.session['usuario'] = usuario[0].id
    return redirect('home:home')



def sair(request):
    messages.add_message(request, constants.SUCCESS, 'Você saiu do portal!')
    request.session.flush()
    return redirect('home:home')





def editar_perfil(request):
    if request.session.get('usuario'):
        user = Usuario.objects.get(id = request.session['usuario'])
        user.nomeUsuario = request.POST.get('nome')
        user.sobre = request.POST.get('sobre')
        user.genero = request.POST.get('genero')        

            
        user.save()
        
        
        # user.formacao.add(*formacao)
        messages.add_message(request, constants.SUCCESS, 'Usuario atualizado com sucesso!')
        return redirect('usuario:profile')
    else:
        messages.add_message(request, constants.ERROR, 'Usuário não está logado')
        return redirect('home:home')








def recuperar_senha(request):
    email = request.POST.get('email')
    usuario = Usuario.objects.filter(usuarioEmail = email)
    ativado = usuario.filter(is_active = False)

    
    
    if len(usuario) == 0:
        messages.add_message(request, constants.ERROR, 'Email não encontrado!')
        return redirect('home:home')
    
    elif len(ativado) > 0:
        messages.add_message(request, constants.SUCCESS, 'Ative sua conta antes de logar!')
        return redirect('home:home')
    
    else:
        user = Usuario.objects.get(usuarioEmail =email)
        senha_aleatoria = gerar_senha_temporaria()
        senha = sha256(senha_aleatoria.encode()).hexdigest()
        user.senha = senha
        user.save()
        messages.add_message(request, constants.SUCCESS, 'Senha temporaria enviadas para o seu email!')
        path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/email/recuperar_senha.html')
        email_html(path_template, 'Recuperar senha', [email,],senha=senha_aleatoria, username=email)
        
        
        return redirect('home:home')