from django.shortcuts import render, redirect
from .models import *
from blog.models import *
from autenticacao.models import Usuario
import os
from django.contrib.messages import constants
from django.contrib import messages
from django.conf import settings
from autenticacao.utils import *
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    contato = Contatos.objects.get(id=1)
    feedbacks = Feedbacks.objects.all()
    faq = PerguntasFrequentes.objects.all()
    blog = Post.objects.all()
    recent_posts = Post.objects.order_by('-data')
    
    num_respostas = Resposta.objects.all().count()
    num_comentarios = Comentarios.objects.all().count()
    total_comentarios = num_respostas  + num_comentarios
    total_usuario = Usuario.objects.all().count()
    
    print(total_comentarios)

    
    try:
        usuario = request.session.get('usuario')
        request_usuario = Usuario.objects.get(id = usuario ) 
        return render(request, 'empreendeai/home.html', {'contato':contato,'feedbacks':feedbacks,'faq':faq,'blog':blog, 'usuario':request_usuario, 'total_usuario':total_usuario,'total_comentarios':total_comentarios,'recent_posts':recent_posts})
    except:
        return render(request, 'empreendeai/home.html', {'contato':contato,'feedbacks':feedbacks,'faq':faq,'blog':blog, 'total_usuario':total_usuario,'total_comentarios':total_comentarios,'recent_posts':recent_posts })
    
    
    
def contato_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('msg')
        telefone = request.POST.get('subject')
        
        if  not nome.strip():
            messages.add_message(request, constants.ERROR, 'Seu nome não pode esta vazio')
            url = reverse('home:home') + '#form-contato-ancora'
            return HttpResponseRedirect(url) 
        
        if  not telefone.strip():
            messages.add_message(request, constants.ERROR, 'Insira um numero de telefone')
            url = reverse('home:home') + '#form-contato-ancora'
            return HttpResponseRedirect(url) 
        
        if not re.search(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]', email):
            messages.add_message(request, constants.ERROR, 'E-mail Invalido!')
            url = reverse('home:home') + '#form-contato-ancora'
            return HttpResponseRedirect(url) 
        #teste
        if  not mensagem.strip():
            messages.add_message(request, constants.ERROR, 'Mensagem não pode ficar vazia')
            url = reverse('home:home') + '#form-contato-ancora'
            return HttpResponseRedirect(url) 
        
            
    
        #!MUDAR EMAIL
        meu_email = 'emersonempreender18@gmail.com'
        path_template = os.path.join(settings.BASE_DIR, 'empreendeAi/templates/email/email.html')
        email_html(path_template, 'feedback',[meu_email,], email=email, mensagem=mensagem, nome=nome, telefone= telefone)
        messages.add_message(request, constants.ERROR, 'Mensagem enviada com sucesso em breve retornaremos o contato!')
        url = reverse('home:home') + '#form-contato-ancora'
        return HttpResponseRedirect(url) 