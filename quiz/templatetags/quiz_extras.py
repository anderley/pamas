from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=False)
def envio_status(value):
    status = ''
    if value in ['Cancelado', 'Expirado']:
        status = f'<label class="d-flex align-items-center"><i class="text-danger fa fa-ban mr-2"></i>{value}</label>'
    elif value in ['Enviado', 'Preenchendo']:
        status = f'<label class="d-flex align-items-center"><i class="text-info fa fa-info-circle mr-2"></i>{value}</label>'
    elif value == 'Acessado':
        status = f'<label class="d-flex align-items-center"><i class="text-warning fa fa-exclamation-circle mr-2"></i>{value}</label>'
    elif value == 'Finalizado':
        status = f'<label class="d-flex align-items-center"><i class="text-success fa fa-check-circle mr-2"></i>{value}</label>'

    return mark_safe(status)
