from django.db import models


class Planos(models.Model):
    titulo = models.CharField(max_length=80, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    num_formularios = models.IntegerField(verbose_name='Num. Formulários')
    valor = models.FloatField(verbose_name='Valor (R$)')

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'planos'
        verbose_name = 'plano'
        verbose_name_plural = 'planos'
