from django.contrib import admin
from .models import *
# Register your models here.

class AtivacaoEmLinha(admin.StackedInline):
    model = Ativacao
    extra = 0
    
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [AtivacaoEmLinha]


admin.site.register(Usuario, UsuarioAdmin)    
admin.site.register(Ativacao)