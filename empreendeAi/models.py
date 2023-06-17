from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe

# Create your models here.

class Feedbacks(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    funcao = models.CharField(max_length=50, null=False, blank=False)
    mensagem = models.TextField(null=False, blank=False)
    
    def __str__(self) -> str:
        return self.nome
    

class PerguntasFrequentes(models.Model):
    pergunta = models.CharField(max_length=255,null=False, blank=False)
    resposta  = RichTextField()
    
    def __str__(self) -> str:
        return self.pergunta
    

class Contatos(models.Model):
    endereco = models.TextField(null=False, blank=False)
    telefone = models.CharField(max_length=12, null=False, blank=False)
    whatsapp = models.CharField(max_length=12, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    
    def __str__(self) -> str:
        return 'Contato para informações'
    
    #? Metodo para sempre ter apenas um numero cadastro de contatos principal
    def save(self, *args, **Kawargs):
        self.pk =1
        super(Contatos, self).save(*args, **Kawargs)


    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if not created:
            return obj 
        return Contatos(pk=1)