from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Notificacoes(models.Model):

    class Tipo(models.TextChoices):
        INFORMATIVA = 'Informativa', _('Informativa')
        SUCESSO = 'Sucesso', _('Sucesso')
        ALERTA = 'Alerta', _('Alerta')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario') # noqa
    mensagem = models.TextField(verbose_name='Mensagem')
    tipo = models.CharField(max_length=80, choices=Tipo.choices,
        default=Tipo.INFORMATIVA,verbose_name='Tipo')
    is_visualizado = models.BooleanField(default=False, verbose_name='Visualizado') # noqa
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    def __str__(self):
        return self.tipo

    class Meta:
        db_table = 'notificacoes'
        verbose_name = 'notificacao'
        verbose_name_plural = 'notificacoes'
