from django.contrib.auth.models import User
from .models import Client
from django.core.mail import send_mail


def create_user_by_email(strategy, backend, details, response, user=None, *args, **kwargs):
    email = kwargs.get('email') or details.get('email')
    username = kwargs.get('username') or details.get('username')

    first_name = details.get('first_name', None)
    last_name = details.get('last_name', None)

    if not username:
        username = email.split('@')[0]
    try:
        user = User.objects.get(email=email)
        send_mail(
            subject="Nuevo inicio de sesión con tu cuenta de EcoMods",
            message=f"Hola {first_name} {last_name},\nAcabas de iniciar sesión con tu cuenta en EcoMods.\nSi no reconoces esta solicitud, por favor cambia tu contraseña.",
            from_email="ecomodstechnology@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return {'is_new': False, 'user': user}

    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        send_mail(
            subject="Cuenta registrada con éxito",
            message=f"Hola {first_name},\nTu cuenta de EcoMods ha sido asociada a esta cuenta de Google ({email}) exitosamente.",
            from_email="ecomodstechnology@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        credit_card = details.get('credit_card', None)
        Client.objects.create(
            user=user,
            creditCard=credit_card
        )

        return {'is_new': True, 'user': user}
