from typing import List

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailUtils:

    @staticmethod
    def send_email_form(
        email: str,
        link_form: str,
        user: User
    ):
        subject = '[PAMAS] Assessment'
        html_message = render_to_string(
            'quiz/emails/link_form.html',
            {
                'link': link_form
            }
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject, plain_message, settings.EMAIL_HOST_USER,
            [email], html_message=html_message, fail_silently=False
        )

    @staticmethod
    def send_email_pdf(
        to_email: str,
        cc_email: List[str],
        pdf_path: str,
        user_name: User
    ):
        subject = '[PAMAS] Resultado'
        html_content = render_to_string(
            'quiz/emails/send_pdf.html',
            {
                'user_name': user_name,
            }
        )
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
            cc=cc_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.attach_file(pdf_path, 'application/pdf')
        msg.send()
