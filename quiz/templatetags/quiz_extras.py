from django import template


register = template.Library()


@register.filter
def status_class(value):
    if value in ['Cancelado', 'Expirado']:
        return 'danger'
    elif value in ['Enviado', 'Preenchendo']:
        return 'info'
    elif value == 'Acessado':
        return 'warning'
    elif value == 'Finalizado':
        return 'success'
    return ''
