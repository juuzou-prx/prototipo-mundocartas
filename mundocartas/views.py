from django.conf import settings
from django.http import Http404
from django.shortcuts import render


# Handlers de error. Se registran en mundocartas/urls.py (handler400/403/404)
# y en settings.py (CSRF_FAILURE_VIEW). El 500 lo resuelve Django solo con templates/500.html.

def error_400(request, exception=None):
    return render(request, '400.html', status=400)


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def csrf_failure(request, reason=''):
    # el detalle técnico solo se muestra en desarrollo
    return render(request, '403_csrf.html', {'reason': reason if settings.DEBUG else ''}, status=403)


# Solo para desarrollo: permite ver cada página con DEBUG=True (/probar-error/404/, etc.)
PAGINAS = {
    '400': ('400.html', 400),
    '403': ('403.html', 403),
    'csrf': ('403_csrf.html', 403),
    '404': ('404.html', 404),
    '405': ('405.html', 405),
    '500': ('500.html', 500),
}


def probar_error(request, codigo):
    if codigo not in PAGINAS:
        raise Http404
    plantilla, estado = PAGINAS[codigo]
    return render(request, plantilla, status=estado)
