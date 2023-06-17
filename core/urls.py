from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from autenticacao.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("empreendeAi.urls", namespace="home")),
    path('blog/', include("blog.urls", namespace="blog")),
    path('autenticacao/', include("autenticacao.urls", namespace="autenticacao")),
    path('usuario/', include("usuario.urls", namespace="usuario")),
   
    
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
#? Arquivos estaticos
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)