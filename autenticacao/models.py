from django.db import models

# Create your models here.
class Usuario(models.Model):
    userName = models.CharField(max_length=100, null=False, blank=False)
    nomeUsuario =  models.CharField(max_length=100, null=True, blank=True)
    usuarioEmail  =  models.CharField(max_length=100, null=False, blank=False)
    senha = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.userName
    
    
class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.userName