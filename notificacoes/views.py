from django.views.generic import TemplateView, ListView
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notificacoes


class NotificacoesJsonView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        notificacoes = Notificacoes.objects.order_by('-created_at').all()[:10]
        count = Notificacoes.objects.filter(is_visualizado=False).count()

        context = {
            'data': [
                notificacao
                for notificacao in notificacoes.values()
            ],
            'count': count
        }

        return JsonResponse(context, safe=False)


class NotificacoesListView(LoginRequiredMixin, ListView):
    model = Notificacoes
    template_name = 'notificacoes/listar.html'

