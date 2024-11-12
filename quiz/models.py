from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Grupos(models.Model):
    nome = models.CharField(max_length=80)
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'grupos'
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'


class Competencias(models.Model):
    nome = models.CharField(max_length=180)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'competencias'
        verbose_name = 'competencia'
        verbose_name_plural = 'competencias'


class Perguntas(models.Model):
    descricao = models.TextField(verbose_name='Descrição')
    competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name='Competência') # noqa
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    @property
    def grupo(self):
        return self.competencia.grupo

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'perguntas'
        verbose_name = 'pergunta'
        verbose_name_plural = 'perguntas'


class Textos(models.Model):
    texto = models.TextField(verbose_name='Texto')
    competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name='Competência') # noqa
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado') # noqa
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado') # noqa

    def __str__(self):
        return self.texto

    class Meta:
        db_table = 'textos'
        verbose_name = 'texto'
        verbose_name_plural = 'textos'


class Contatos(models.Model):
    nome_completo = models.CharField(max_length=180, verbose_name='Nome Completo') # noqa
    email = models.EmailField(max_length=180, unique=True, verbose_name='Email') # noqa
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario') # noqa
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado') # noqa
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado') # noqa

    def __str__(self):
        return self.nome_completo

    class Meta:
        db_table = 'contatos'
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'


class FomularioClientes(models.Model):

    class Status(models.TextChoices):
        ENVIADO = 'Enviado', _('Enviado')
        ACESSADO = 'Acessado', _('Acessado')
        PREENCHENDO = 'Preenchendo', _('Preenchendo')
        FINALIZADO = 'Finalizado', _('Finalizado')
        EXPIRADO = 'Expirado', _('Expirado')
        CANCELADO = 'Cancelado', _('Cancelado')
        ENCERRADO = 'Encerrado', _('Encerrado')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario') # noqa
    email = models.EmailField(max_length=180, verbose_name='Email')
    token = models.CharField(max_length=180, verbose_name='Token')
    form_url = models.CharField(max_length=250, verbose_name='URL Formulário')
    status = models.CharField(
        max_length=80, choices=Status.choices, default=Status.ENVIADO
    )
    iniciado = models.DateTimeField(blank=True, null=True, verbose_name='Inicio Preenchimento') # noqa
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    @property
    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'formulario_clientes'
        verbose_name = 'formulario_cliente'
        verbose_name_plural = 'formulario_clientes'


class Respostas(models.Model):
    resposta = models.IntegerField(default=0, verbose_name='Resposta')
    pergunta = models.ForeignKey(Perguntas, on_delete=models.CASCADE, verbose_name='Pergunta') # noqa
    formulario = models.ForeignKey(FomularioClientes, on_delete=models.CASCADE, verbose_name='Formulario') # noqa
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado')

    class Meta:
        db_table = 'respostas'
        verbose_name = 'resposta'
        verbose_name_plural = 'respostas'
        constraints = [
            models.UniqueConstraint(fields=['formulario', 'pergunta'], name='unique_respostas') # noqa
        ]
