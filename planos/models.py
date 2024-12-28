from django.db import models
from django.utils import formats


class Planos(models.Model):
    titulo = models.CharField(max_length=80, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    num_formularios = models.IntegerField(verbose_name='Num. Formulários')
    valor = models.FloatField(verbose_name='Valor (R$)')
    parcelas = models.IntegerField(verbose_name='Número de parcelas', default=1)

    def __str__(self):
        return self.titulo
    
    def formatar_valor(self):
        return f"{formats.number_format(self.valor, 2, ',', '.')}"

    class Meta:
        db_table = 'planos'
        verbose_name = 'plano'
        verbose_name_plural = 'planos'
