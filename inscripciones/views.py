import time
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.utils import timezone
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction
from torneos.models import Torneo
from .models import Inscripcion, Pago, Asistencia

@login_required
def inscribirse(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    if request.method == 'POST':
        if torneo.estado != 'programado':
            messages.error(request, 'Este torneo no admite inscripciones.')
        elif torneo.inscripciones.filter(estado='activa').count() >= torneo.cupo_maximo:
            messages.error(request, 'El cupo de este torneo está lleno.')
        else:
            insc, creada = Inscripcion.objects.get_or_create(usuario=request.user, torneo=torneo)
            if creada:
                messages.success(request, 'Te inscribiste correctamente.')
            elif insc.estado == 'cancelada':
                insc.estado = 'activa'
                insc.save()
                messages.success(request, 'Te inscribiste correctamente.')
            else:
                messages.info(request, 'Ya estás inscrito en este torneo.')
    return redirect('torneo_detalle', pk=torneo.pk)


@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(
        usuario=request.user, estado='activa'
    ).select_related('torneo__juego')
    return render(request, 'inscripciones/mis_inscripciones.html', {'inscripciones': inscripciones})


@login_required
def cancelar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk, usuario=request.user, estado='activa')
    if request.method == 'POST':
        inscripcion.estado = 'cancelada'
        inscripcion.save()
        messages.success(request, 'Tu inscripción fue cancelada.')
        return redirect('mis_inscripciones')
    return render(request, 'inscripciones/cancelar_inscripcion.html', {'inscripcion': inscripcion})


@staff_member_required(login_url='iniciar_sesion')
def lista_inscritos(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    activas = torneo.inscripciones.filter(estado='activa')
    for i in activas:
        Pago.objects.get_or_create(inscripcion=i, defaults={'monto': torneo.costo})
        Asistencia.objects.get_or_create(inscripcion=i)
    inscripciones = activas.select_related('usuario', 'pago', 'asistencia')
    return render(request, 'inscripciones/lista_inscritos.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
    })

def _webpay_transaction():
    if not settings.WEBPAY_COMMERCE_CODE or not settings.WEBPAY_API_KEY:
        raise ImproperlyConfigured("Faltan WEBPAY_COMMERCE_CODE o WEBPAY_API_KEY en el .env")
    ambiente = IntegrationType.LIVE if settings.WEBPAY_ENV == 'LIVE' else IntegrationType.TEST
    options = WebpayOptions(
        commerce_code=settings.WEBPAY_COMMERCE_CODE,
        api_key=settings.WEBPAY_API_KEY,
        integration_type=ambiente,
    )
    return Transaction(options)


@login_required
def iniciar_pago(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id, usuario=request.user, estado='activa')
    pago, _ = Pago.objects.get_or_create(inscripcion=inscripcion, defaults={'monto': inscripcion.torneo.costo})
    if pago.estado == 'pagado':
        messages.info(request, 'Esta inscripción ya está pagada.')
        return redirect('mis_inscripciones')
    if pago.monto <= 0:
        messages.info(request, 'Este torneo no tiene costo de inscripción.')
        return redirect('mis_inscripciones')
    request.session['pago_id'] = pago.id
    buy_order = f"i{inscripcion.id}-{int(time.time())}"
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri(reverse('pago_exitoso'))
    try:
        tx = _webpay_transaction()
        response = tx.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=pago.monto,
            return_url=return_url,
        )
        return redirect(f"{response['url']}?token_ws={response['token']}")
    except Exception as e:
        messages.error(request, f"Error al iniciar el pago: {e}")
        return redirect('mis_inscripciones')


@login_required
def pago_exitoso(request):
    pago_id = request.session.pop('pago_id', None)
    if not pago_id:
        messages.info(request, 'Este pago ya fue procesado.')
        return redirect('mis_inscripciones')
    pago = get_object_or_404(Pago, pk=pago_id, inscripcion__usuario=request.user)
    if request.GET.get('TBK_TOKEN'):
        messages.warning(request, 'Cancelaste el pago.')
        return redirect('mis_inscripciones')
    token = request.GET.get('token_ws')
    if not token:
        messages.error(request, 'No se recibió el token de Webpay.')
        return redirect('mis_inscripciones')
    try:
        tx = _webpay_transaction()
        response = tx.commit(token)
        status = response.get('status')
    except Exception as e:
        messages.error(request, f"Error al confirmar el pago: {e}")
        return redirect('mis_inscripciones')
    if status != 'AUTHORIZED':
        messages.warning(request, f"El pago no fue autorizado ({status}).")
        return redirect('mis_inscripciones')
    pago.estado = 'pagado'
    pago.fecha_pago = timezone.now()
    pago.save()
    return render(request, 'inscripciones/pago_exitoso.html', {'pago': pago, 'response': response})

@staff_member_required(login_url='iniciar_sesion')
def cambiar_pago(request, pago_id):
    pago = get_object_or_404(Pago, pk=pago_id)
    if request.method == 'POST':
        if pago.estado == 'pendiente':
            pago.estado = 'pagado'
            pago.fecha_pago = timezone.now()
            pago.registrado_por = request.user
            messages.success(request, 'Pago registrado como pagado.')
        else:
            pago.estado = 'pendiente'
            pago.fecha_pago = None
            pago.registrado_por = None
            messages.info(request, 'Pago marcado como pendiente.')
        pago.save()
    return redirect('lista_inscritos', torneo_id=pago.inscripcion.torneo_id)

@staff_member_required(login_url='iniciar_sesion')
def cambiar_participacion(request, asistencia_id):
    asistencia = get_object_or_404(Asistencia, pk=asistencia_id)
    if request.method == 'POST':
        asistencia.participo = not asistencia.participo
        asistencia.fecha_registro = timezone.now() if asistencia.participo else None
        asistencia.save()
        messages.success(request, 'Participación actualizada.')
    return redirect('lista_inscritos', torneo_id=asistencia.inscripcion.torneo_id)    