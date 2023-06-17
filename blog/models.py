from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from PIL import Image
from autenticacao.models import Usuario
from datetime import datetime
# Create your models here.

class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    tema = models.CharField(max_length=255, null=False, blank=False)
    titulo = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    post = RichTextField()
    data = models.DateTimeField(default = datetime.now)
    
    def __str__(self) -> str:
        return self.titulo
    
    

class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    comentario = models.TextField()
    data = models.DateTimeField(default = datetime.now)
    pos = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='comentarios')

    def __str__(self) -> str:
        return self.usuario.userName
    
    
class Resposta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    data = models.DateTimeField(default=datetime.now)
    comentario_pai = models.ForeignKey(Comentarios, on_delete=models.CASCADE, related_name='respostas')

    def __str__(self):
        return self.usuario.userName