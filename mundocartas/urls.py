from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from torneos import views as torneos_view
from mundocartas import views as error_views

handler400 = 'mundocartas.views.error_400'
handler403 = 'mundocartas.views.error_403'
handler404 = 'mundocartas.views.error_404'
handler500 = 'mundocartas.views.error_500'

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
    urlpatterns += [path('probar-error/<str:codigo>/', error_views.probar_error)]