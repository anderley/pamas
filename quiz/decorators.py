import functools
import logging

from typing import Any, Callable

from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied

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
        token: RequestToken | None = getattr(request, 'token', None)
        
        try:
            token.validate_max_uses()
            token.authenticate(request)

        except Exception as e:
            if 'rt' in request.GET:
                token = request.GET['rt']
                form_cliente = FomularioClientes.objects.get(token=token)

                print (form_cliente)
                form_cliente.status = 'Expirado'
                form_cliente.save()
        
        return view_func(*args, **kwargs)

    return inner
