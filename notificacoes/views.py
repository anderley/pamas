import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import ListView, TemplateView

from .models import Notificacoes


@login_required(redirect_field_name='login')
def set_viewed_notificacao(request):
    if request.method == 'PUT':
        payload = json.loads(request.body.decode('utf-8'))
        notificacoes = Notificacoes.objects.filter(id__in=payload['ids'])

        for notificacao in notificacoes:
            notificacao.is_visualizado = True

        Notificacoes.objects.bulk_update(notificacoes, ['is_visualizado'])

    return HttpResponse(status=201)


class NotificacoesJsonView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        query = Notificacoes.objects.filter(
            is_visualizado=False,
            user=request.user
        )
        context = {
            'data': [
                notificacao
                for notificacao in query.all()[:10].values()
            ],
            'count': query.count()
        }

        return JsonResponse(context, safe=False)


class NotificacoesListView(LoginRequiredMixin, ListView):
    model = Notificacoes
    template_name = 'notificacoes/listar.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        ).order_by('-created_at')
