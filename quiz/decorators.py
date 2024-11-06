import functools
import logging
from typing import Any, Callable
from datetime import datetime, timedelta

from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.conf import settings

from request_token.exceptions import TokenNotFoundError
from request_token.models import RequestToken

from .models import FomularioClientes, Contatos
from notificacoes.models import Notificacoes

logger = logging.getLogger(__name__)


def _get_request_arg(*args: Any) -> HttpRequest | None:
    for arg in args:
        if isinstance(arg, HttpRequest):
            return arg
    return None


def use_request_token_check_expiration(
    view_func: Callable | None = None,
    required: bool = True,
) -> Callable:
    
    if view_func is None:
        return functools.partial(
            use_request_token, scope=scope, required=required, log=log
        )

    @functools.wraps(view_func)
    def inner(*args, **kwargs):
        request = _get_request_arg(*args)
        token = request.GET['rt']
        request_token: RequestToken | None = getattr(request, 'token', None)

        if request_token is None:
            if required is True:
                raise TokenNotFoundError()

        form_cliente = FomularioClientes.objects.get(token=token)

        try:
            request_token.validate_max_uses()
            request_token.authenticate(request)

            logger.info('Token valido!')

            # verifica se o token foi cancelado
            if form_cliente.status == FomularioClientes.Status.CANCELADO:
                logger.info('Token cancelado pelo usuário!')

                return render(request, '403.html')
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


def timeout_form(
        view_func: Callable | None = None
) -> Callable:
    
    @functools.wraps(view_func)
    def inner(*args, **kwargs):
        if 'pk' in kwargs:
            form_cliente = FomularioClientes.objects.get(id=kwargs['pk'])

            if form_cliente.iniciado:
                max_time = form_cliente.iniciado + timedelta(minutes=settings.TIMEOUT_FORMULARIO)

                if (
                    max_time.replace(tzinfo=None) < datetime.now().replace(tzinfo=None)
                    and form_cliente.status != FomularioClientes.Status.FINALIZADO
                ):
                    form_cliente.status = FomularioClientes.Status.ENCERRADO
                    form_cliente.save()
                    
                    data_envio = form_cliente.created_at.strftime(settings.DATE_FORMAT_DEFAULT)
                    Notificacoes(
                        user=form_cliente.user,
                        mensagem=f'O Formulario enviado para {form_cliente.email} na data {data_envio}, cancelado!',
                        tipo=Notificacoes.Tipo.ALERTA
                    ).save()

                    request = _get_request_arg(args)
                
                    return render(request, 'quiz/timout_form.html')

        return view_func(*args, **kwargs)

    return inner


def check_contato(
        view_func: Callable | None = None
) -> Callable:
    
    @functools.wraps(view_func)
    def inner(*args, **kwargs):
        if 'pk' in kwargs:
            form_cliente = FomularioClientes.objects.get(id=kwargs['pk'])
            contato = Contatos.objects.filter(email=form_cliente.email)

            if not contato.exists():
                return redirect(
                    reverse('formulario_cadastro') + f'?rt={form_cliente.token}'
                )

        return view_func(*args, **kwargs)

    return inner
