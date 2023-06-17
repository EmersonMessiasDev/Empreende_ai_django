from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'usuario'

urlpatterns = [
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('perfil/', perfil, name='perfil'),   
    path('delete_usuario_logado/', delete_usuario_logado, name='delete_usuario_logado')
]