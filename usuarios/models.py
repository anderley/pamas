from django.contrib.auth.models import User
from django.db import models
from pagamentos.models import Pagamentos


class UsuarioEnvioFormulario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário') # noqa
    pagamento = models.ForeignKey(Pagamentos, on_delete=models.CASCADE, verbose_name='Pagamentos') # noqa
    num_formularios = models.IntegerField(default=0)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.pagamento, self.num_formularios)

    class Meta:
        db_table = 'usuarios_envio_formulario'
        verbose_name = 'usuário - envio de formulário'
        verbose_name_plural = 'usuários - envio de formulário'
