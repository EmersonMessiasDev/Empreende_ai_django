from django.shortcuts import redirect, render
from autenticacao.models import *
from empreendeAi.models import *
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages import constants
from django.contrib import messages
# Create your views here.

def blog(request, page=1):
    contato = Contatos.objects.get(id=1)
    blog = Post.objects.all()
    paginator = Paginator(blog, 6)
    
    page_obj = paginator.get_page(page)
    
    try:
        usuario = request.session.get('usuario')
        request_usuario = Usuario.objects.get(id = usuario ) 
        return render(request, 'blog/blog.html', {'contato':contato,'blog':blog, 'page_obj': page_obj,'usuario':request_usuario})
    except:
        return render(request, 'blog/blog.html', {'contato':contato,'blog':blog, 'page_obj': page_obj })



def blog_detalhe(request, id):
    contato = Contatos.objects.get(id=1)
    blog = Post.objects.order_by('-data')
    post = Post.objects.get(id=id)
    comentario = Comentarios.objects.filter(pos_id=id)
    resposta = Resposta.objects.filter(comentario_pai__in=comentario)
    
    
    
    
    
    total_comentarios = comentario.count() + resposta.count()

   
    if request.session.get('usuario'): 
        usuario = request.session.get('usuario')
        request_usuario = Usuario.objects.get(id = usuario )      
        
        context ={
            'post':post,
            'comentario':comentario,
            'contato':contato,
            'blog':blog,
            'usuario_resposta': request_usuario if request.session.get('usuario') else None,
            'usuario':request_usuario,
            'total_comentarios':total_comentarios
        }
    else:
         context ={
            'post':post,
            'comentario':comentario,
            'contato':contato,
            'blog':blog,
            'total_comentarios':total_comentarios
        }
    
    
    return render(request, 'blog/blog-detalhe.html', context)


def excluir_comentario(request, tipo, id):
    if request.method == 'POST':
        if tipo == 'comentario':
            comentario = Comentarios.objects.get(id=id)
            if comentario.usuario_id == request.session.get('usuario'):
                comentario.delete()
                messages.add_message(request, constants.SUCCESS, 'Comentario excluido com sucesso!')
                redirect_url = reverse('blog:blog_detalhe', kwargs={'id': comentario.pos_id}) + '#ancora'
                return HttpResponseRedirect(redirect_url)
        elif tipo == 'resposta':
            resposta = Resposta.objects.get(id=id)
            if resposta.usuario_id == request.session.get('usuario'):
                resposta.delete()
                messages.add_message(request, constants.SUCCESS, 'Comentario excluido com sucesso!')
                redirect_url = reverse('blog:blog_detalhe', kwargs={'id': resposta.comentario_pai.pos_id}) + '#ancora'
                return HttpResponseRedirect(redirect_url)


def adicionar_comentario(request, id):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario')
        comentario = request.POST['comentario']
        post_id = id
        
        comentario_obj = Comentarios(usuario_id=usuario_id, comentario=comentario, pos_id=post_id)
        comentario_obj.save()
        messages.add_message(request, constants.SUCCESS, 'Comentario enviado com sucesso!')
        
        redirect_url = reverse('blog:blog_detalhe', kwargs={'id': id}) + f'#ancora'
        return HttpResponseRedirect(redirect_url)


def responder_comentario(request):
    if request.method == 'POST':
        usuario = request.session.get('usuario')
        comentario_pai_id = request.POST.get('comentario_pai')
        resposta_texto = request.POST.get('resposta')
        messages.add_message(request, constants.SUCCESS, 'Comentario enviado com sucesso!')
        # Salvar a resposta no banco de dados, relacionando-a com o comentário pai
        resposta = Resposta.objects.create(usuario_id=usuario, comentario=resposta_texto, comentario_pai_id=comentario_pai_id)

        redirect_url = reverse('blog:blog_detalhe', kwargs={'id': resposta.comentario_pai.pos_id}) + f'#ancora'
        return HttpResponseRedirect(redirect_url)
    
    
from .models import Post

def pesquisa(request):
    contato = Contatos.objects.get(id=1)
    query = request.GET.get('q')
    print(f"Query: {query}")
    if query:  # se 'query' não está vazia
        results = Post.objects.filter(titulo__icontains=query)
        found = results.exists()  # verifica se há algum resultado
    else:  # se 'query' está vazia
        results = Post.objects.none()  # retorna um QuerySet vazio
        found = False  # considera que não há resultados
    try:

        usuario = request.session.get('usuario')
        request_usuario = Usuario.objects.get(id = usuario ) 
        return render(request, 'blog/search_results.html', {'results': results, 'found': found, 'contato':contato,'usuario':request_usuario})
    except:
        return render(request, 'blog/search_results.html', {'results': results, 'found': found, 'contato':contato})
