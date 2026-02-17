from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importamos a nova função 'filtrar_categoria'
from blog.views import home, detalhe_noticia, filtrar_categoria

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('noticia/<int:id>/', detalhe_noticia, name='detalhe'),
    
    # NOVA ROTA: O <str:nome> pega o texto (ex: SAUDE, MUNDO)
    path('categoria/<str:nome>/', filtrar_categoria, name='filtro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)