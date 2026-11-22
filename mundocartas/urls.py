from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from torneos import views as torneos_view

urlpatterns = [
    path('', torneos_view.torneo_lista, name='inicio'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('torneos/', include('torneos.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('resultados/', include('resultados.urls')),
    path('recompensas/', include('recompensas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)