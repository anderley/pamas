from django.contrib.auth.models import User
from django.db import models

CHOICES = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('rejeitado', 'Rejeitado'),
]


class Pagamentos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário') # noqa
    mercadopago_id = models.CharField(max_length=80, verbose_name='Mercado Pago ID', null=True) # noqa
    plano_titulo = models.CharField(max_length=80, verbose_name='Plano - Título') # noqa
    plano_descricao = models.TextField(verbose_name='Plano - Descrição') # noqa
    plano_num_formularios = models.IntegerField(verbose_name='Plano - Num. Formulários') # noqa
    plano_valor = models.FloatField(verbose_name='Plano - Valor (R$)')
    status = models.CharField(max_length=10, choices=CHOICES)
    criado = models.DateTimeField(auto_now_add=True, editable=False)
    modificado = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return 'Pagamento {}'.format(self.pk)

    class Meta:
        db_table = 'pagamentos'
        verbose_name = 'pagamento'
        verbose_name_plural = 'pagamentos'
