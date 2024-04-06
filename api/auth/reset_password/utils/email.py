from django.core.mail import EmailMessage
from django.conf import settings


def send_email_reset_password(email, username, token):
    title = 'Сброс пароля'
    link = f'{settings.FRONTEND_HOST}/reset-password/{token}'
    message = f'Для сброса пароля перейдите по ссылке: {link}. Ваш логин: {username}'
    email = EmailMessage(title, message, to=[email])
    email.send()
