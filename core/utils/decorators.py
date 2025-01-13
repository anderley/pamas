from django.contrib.auth import logout
from django.shortcuts import redirect
from functools import wraps
from urllib.parse import urlencode
from django.urls import reverse


def deslogar_se_admin(view_func):
    def wrapper(request, *args, **kwargs):

        # Verificar se o usuário é um superusuário (admin)
        if request.user.is_authenticated:
            logout(request)  # Realizar o logout

            # # Redirecionar para a página de login, mantendo a URL original
            # next_url = request.get_full_path()  # Captura a URL atual
            # login_url = reverse("login")  # Obter a URL para a página de login
            # if next_url:
            #     login_url = f'{login_url}?{urlencode({"next": next_url})}'  # Adicionar o parâmetro next
            #
            # return redirect(login_url)  # Redirecionar para login com o parâmetro next

        response = view_func(request, *args, **kwargs)
        return response
    return wrapper