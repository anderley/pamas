from django.db import models
from django.contrib import admin


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
    descricao = models.TextField()
    vm = models.IntegerField()
    competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao
    
    def grupo(self):
        return self.competencia.grupo

    class Meta:
        db_table = 'perguntas'
        verbose_name = 'pergunta'
        verbose_name_plural = 'perguntas'


# Register models to django admin
admin.site.register(Grupos)
admin.site.register(Competencias, list_display=['nome', 'grupo'])
admin.site.register(Perguntas, list_display=['descricao', 'competencia', 'grupo'])