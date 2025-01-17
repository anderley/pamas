from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from pagamentos.models import Pagamentos


class UsuarioEnvioFormulario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário') # noqa
    pagamento = models.ForeignKey(Pagamentos, on_delete=models.CASCADE, verbose_name='Pagamentos', null=True) # noqa
    num_formularios = models.IntegerField(default=0)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.pagamento, self.num_formularios) # noqa

    class Meta:
        db_table = 'usuarios_envio_formulario'
        verbose_name = 'usuário - envio de formulário'
        verbose_name_plural = 'usuários - envio de formulário'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=20, verbose_name='Whatsapp')

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user_profile'
        verbose_name_plural = 'user_profiles'

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, raw, **kwargs):
        if raw:
            profile = instance.userprofile
            profile.user = instance
            profile.save()
