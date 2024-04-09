from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from jwt_auth.models import User


def send_email(user: User):
    token = default_token_generator.make_token(user)
    verify_email_link = f'{settings.VERIFY_EMAIL_URL}?user_id={user.id}&token={token}'
    user.email_user(
        'Активация аккаунта',
        '',
        html_message=f'Перейдите по ссылке, чтобы активировать аккаунт:\n'
                     f'<a href="{verify_email_link}">{verify_email_link}</a>'
    )
