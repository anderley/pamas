from django.db import models


class Grupos(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'grupos'
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'


class Competencias(models.Model):
    nome = models.CharField(max_length=180)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'competencias'
        verbose_name = 'competencia'
        verbose_name_plural = 'competencias'


class Perguntas(models.Model):
    descricao = models.TextField(verbose_name='Descrição')
    competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name='Competência')

    def __str__(self):
        return self.descricao
    
    def grupo(self):
        return self.competencia.grupo

    class Meta:
        db_table = 'perguntas'
        verbose_name = 'pergunta'
        verbose_name_plural = 'perguntas'


class Textos(models.Model):
    texto = models.TextField(verbose_name='Texto')
    competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name='Competência')

    def __str__(self):
        return self.texto

    class Meta:
        db_table = 'textos'
        verbose_name = 'texto'
        verbose_name_plural = 'textos'
