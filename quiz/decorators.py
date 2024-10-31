import functools
import logging

from typing import Any, Callable

from django.http import HttpRequest
from django.shortcuts import render

from request_token.models import RequestToken

from .models import FomularioClientes


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
        if form_cliente.status == 'Cancelado':
            logger.info('Token cancelado pelo usuário!')

            return render(request, '403.html')

        try:
            request_token.validate_max_uses()
            request_token.authenticate(request)

            logger.info('Token valido!')
        except Exception as e:
            # token expirado
            form_cliente.status = 'Expirado'

            logger.info('Token expirou!')

            return render(request, '403.html')
            
        form_cliente.save()
        
        return view_func(*args, **kwargs)

    return inner
