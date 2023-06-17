from django.contrib import admin
from .models import *

# Register your models here.

class ComentariosEmLinhas(admin.StackedInline):
    model = Comentarios
    
   
class PostAdmin(admin.ModelAdmin):
    inlines = [ComentariosEmLinhas, ]
    
admin.site.register(Post, PostAdmin)
admin.site.register(Resposta)
