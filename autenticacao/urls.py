from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'autenticacao'

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('validar_login/', validar_login, name='validar_login'),
    path('sair/', sair, name = 'sair'),
    path('ativar_conta/<str:token>/', ativar_conta, name="ativar_conta"),
    path('recuperar_senha/', recuperar_senha, name="recuperar_senha"),
    path('logar/', logar, name="logar"),    
    path('cadastrar/', cadastrar, name="cadastrar")    
]