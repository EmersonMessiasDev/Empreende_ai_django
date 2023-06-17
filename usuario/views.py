from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from autenticacao.utils import email_html, password_is_valid, Alterar_senha
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

# Create your views here.

def perfil(request):
    contato = Contatos.objects.get(id=1)
    usuario = request.session.get('usuario')
    request_usuario = Usuario.objects.get(id = usuario )
    
    context = {'contato':contato, 'usuario':request_usuario} 
    return render(request, 'usuario/perfil.html', context)


def alterar_senha(request):
    usuario_id = request.session.get('usuario')
    
    if usuario_id is None:
        messages.error(request, 'Usuário não está logado')
        return redirect('home:home')

    try:
        user = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado')
        return redirect('home:home')
    
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    
    if not Alterar_senha(request, senha, confirmar_senha):
        return redirect('usuario:perfil')

    if senha != confirmar_senha:
        messages.error(request, 'As senhas não correspondem')
        return redirect('usuario:perfil')
    
    try:
        senha_hashed = sha256(senha.encode()).hexdigest()
        user.senha = senha_hashed
        user.save()
        messages.success(request, 'Senha alterada com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao tentar redefinir senha: {e}')
    
    return redirect('usuario:perfil')



def delete_usuario_logado(request):
    usuario_id = request.session.get('usuario')
    
    confirmar = request.POST.get('accountActivation')
    
    print(confirmar)
    
    if usuario_id is None:
        messages.error(request, 'Usuário não está logado')
        return redirect('home:home')
    elif confirmar != 'on':
        messages.error(request, 'Confirme a exclusão da sua conta')
        return redirect('usuario:perfil')
    else:
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.delete()
        del request.session['usuario']  # Remover o usuário da sessão após deletá-lo
        messages.success(request, 'Usuário deletado com sucesso.')
        return redirect('home:home')