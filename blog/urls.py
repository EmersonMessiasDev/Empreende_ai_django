from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = 'blog'

urlpatterns = [
    path('', blog, name='blog'),
    path('posts/page/<int:page>/', blog, name='posts_page'),
    path('blog-detalhe/<int:id>', blog_detalhe, name='blog_detalhe'),
    path('responder_comentario/', responder_comentario, name='responder_comentario'),
    path('comentario/adicionar/<int:id>/', adicionar_comentario, name='adicionar_comentario'),
    path('comentario/excluir/<str:tipo>/<int:id>/', excluir_comentario, name='excluir_comentario'),
    path('pesquisa/', pesquisa, name='pesquisa')

    
    
]