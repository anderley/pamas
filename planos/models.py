from django.db import models
from django.utils import formats
from tinymce import models as tinymce_models


class Planos(models.Model):
    titulo = models.CharField(max_length=80, verbose_name='Título')
    descricao = tinymce_models.HTMLField(verbose_name='Descrição')
    imagem = models.ImageField(upload_to='planos', blank=True, verbose_name='Ícone') # noqa
    cod_cor = models.CharField(max_length=7, default='#000', verbose_name='Cód. Cor') # noqa
    num_formularios = models.IntegerField(verbose_name='Num. Formulários')
    valor = models.FloatField(verbose_name='Valor (R$)')
    parcelas = models.IntegerField(verbose_name='Número de parcelas', default=1) # noqa

    def __str__(self):
        return self.titulo

    def formatar_valor(self):
        return f"{formats.number_format(self.valor, 2, ',', '.')}"

    class Meta:
        db_table = 'planos'
        verbose_name = 'plano'
        verbose_name_plural = 'planos'
