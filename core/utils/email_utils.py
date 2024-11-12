from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailUtils:

    @staticmethod
    def send_email_form(
        email: str,
        link_form: str,
        user: User
    ):
        subject = '[PAMAS] Formulário'
        html_message = render_to_string(
            'quiz/emails/link_form.html',
            {
                'user_name': f'{user.first_name} {user.last_name}',
                'link': link_form
            }
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message # noqa
        )
