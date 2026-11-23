from django.shortcuts import render


class Error405Middleware:
    """Django no tiene handler para el 405 (método no permitido, p. ej. @require_POST
    abierto por GET). Este middleware cambia esa respuesta por templates/405.html."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 405:
            return render(request, '405.html', status=405)
        return response
