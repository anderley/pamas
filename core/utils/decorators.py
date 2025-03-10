
from django.contrib.auth import logout


def deslogar(view_func):
    def wrapper(request, *args, **kwargs):

        # Verificar se o usuário é um superusuário (admin)
        if request.user.is_authenticated:
            logout(request)  # Realizar o logout

            # # Redirecionar para a página de login, mantendo a URL original
            # next_url = request.get_full_path()  # Captura a URL atual
            # login_url = reverse("login")  # Obter a URL para a página de login # noqa
            # if next_url:
            #     login_url = f'{login_url}?{urlencode({"next": next_url})}'  # Adicionar o parâmetro next # noqa
            #
            # return redirect(login_url)  # Redirecionar para login com o parâmetro next # noqa

        response = view_func(request, *args, **kwargs)
        return response
    return wrapper


def deslogar_se_admin(view_func):
    def wrapper(request, *args, **kwargs):

        # Verificar se o usuário é um superusuário (admin)
        if request.user.is_superuser:
            logout(request)  # Realizar o logout

        response = view_func(request, *args, **kwargs)
        return response
    return wrapper
