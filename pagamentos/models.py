from django.db import models
from django.contrib.auth.models import User

CHOICES = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
]

class Pagamentos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    mercadopago_id = models.CharField(max_length=80, verbose_name='Mercado Pago ID', null=True)
    plano_titulo = models.CharField(max_length=80, verbose_name='Plano - Título')
    plano_descricao = models.TextField(verbose_name='Plano - Descrição')
    plano_num_formularios = models.IntegerField(verbose_name='Plano - Num. Formulários')
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
