from django.contrib.auth.models import User
from .models import Client

def create_user_by_email(strategy, backend, details, response, user=None, *args, **kwargs):
    email = kwargs.get('email') or details.get('email')
    username = kwargs.get('username') or details.get('username')

    if not username:
        username = email.split('@')[0]

    try:
        client = Client.objects.get(email=email)

        return {'is_new': False, 'user': client}

    except User.DoesNotExist:
        first_name = details.get('first_name', None)
        last_name = details.get('last_name', None)
        credit_card = details.get('credit_card', None)
        client = Client.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            creditCard=credit_card
        )
        return {'is_new': True, 'user': client}
