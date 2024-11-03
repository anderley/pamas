import functools
import logging
from typing import Any, Callable

from django.http import HttpRequest
from django.shortcuts import render
from django.conf import settings

from request_token.models import RequestToken

from .models import FomularioClientes
from notificacoes.models import Notificacoes

logger = logging.getLogger(__name__)


def _get_request_arg(*args: Any) -> HttpRequest | None:
    """Extract the arg that is an HttpRequest object."""
    for arg in args:
        if isinstance(arg, HttpRequest):
            return arg
    return None


def use_request_token_check_expiration(
    view_func: Callable | None = None,
) -> Callable:

    @functools.wraps(view_func)
    def inner(*args, **kwargs):
        request = _get_request_arg(*args)
        token = request.GET['rt']
        request_token: RequestToken | None = getattr(request, 'token', None)
        form_cliente = FomularioClientes.objects.get(token=token)

        # verifica se o token foi cancelado
        if form_cliente.status == FomularioClientes.Status.CANCELADO:
            logger.info('Token cancelado pelo usuário!')

            return render(request, '403.html')

        try:
            request_token.validate_max_uses()
            request_token.authenticate(request)

            logger.info('Token valido!')
        except Exception:
            # token expirado
            form_cliente.status = FomularioClientes.Status.EXPIRADO
            data_envio = form_cliente.created_at.strftime(settings.DATE_FORMAT_DEFAULT)
            Notificacoes(
                user=form_cliente.user,
                mensagem=f'O Formulario enviado para {form_cliente.email} na data {data_envio}, expirou!',
                tipo=Notificacoes.Tipo.ALERTA
            ).save()

            logger.info('Token expirou!')

            return render(request, '403.html')

        form_cliente.save()

        return view_func(*args, **kwargs)

    return inner
