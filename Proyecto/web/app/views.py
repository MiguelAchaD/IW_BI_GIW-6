from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from app.models import Client
from django.core.mail import send_mail
from smtplib import SMTPException, SMTPAuthenticationError, SMTPSenderRefused, SMTPRecipientsRefused
from socket import error as ConnectionError
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from app.utils import getURL
from django.http import Http404


def index(request):
    return render(request, "index.html")


def logIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if not email.endswith("@gmail.com"):
            return render(request, "accounts/logIn.html", {"errorMessage": "El correo electrónico debe ser de dominio @gmail.com o @opendeusto.es"})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "accounts/logIn.html", {"errorMessage": "Credenciales inválidas"})

    return render(request, "accounts/logIn.html")


def signUp(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirmPassword"]

        if not email.endswith("@gmail.com") and not email.endswith("@opendeusto.es"):
            return render(request, "accounts/signUp.html", {"errorMessage": "El correo electrónico debe ser de dominio @gmail.com o @opendeusto.es"})

        if password != confirm_password:
            return render(request, "accounts/signUp.html", {"errorMessage": "Las contraseñas deben coincidir"})

        token = get_random_string(length=20)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False
            )
            Client.objects.create(user=user, token=token)

        except IntegrityError:
            existing_user = User.objects.get(username=username)
            existing_client = Client.objects.get(user=existing_user)

            if not existing_user.is_active:
                existing_user.email = email
                existing_user.set_password(password)
                existing_user.save()

                existing_client.token = token
                existing_client.save()
            else:
                return render(request, "accounts/signUp.html", {"errorMessage": f"El usuario '{username}' ya está registrado. Inicia sesión con ese usuario o utiliza otro nombre."})

        url = getURL(request)
        if url is None:
            print("Error cargando la URL del usuario")
            return render(request, "accounts/signUp.html", {"errorMessage": "Se ha producido un error cargando la URL"})
        
        try:
            send_mail(
                subject="Autenticación de Correo Electrónico",
                message=f"Haz clic en el siguiente enlace para autenticar tu correo electrónico: {url}/authenticate/newUser?username={username}&token={token}",
                
                from_email="ecomodstechnology@gmail.com",
                recipient_list=[email],
                fail_silently=False
            )
            """
            send_mail(
                subject="Intento de Autenticación de Correo Electrónico",
                message=f"Se está intentando autentificar el correo {email} a través del token '{token}'",
                from_email="ecomodstechnology@gmail.com",
                recipient_list=["diego.merino@opendeusto.es", "miguel.acha@opendeusto.es"],
                fail_silently=False
            )
            """
            return render(request, "accounts/emailConfirmation.html", {"email": email})

        except SMTPException as smtp_exception:
            if isinstance(smtp_exception, SMTPAuthenticationError):
                error_message = "Error de autenticación SMTP."
                print(f"Detalles de error de autenticación SMTP: {smtp_exception}")
            elif isinstance(smtp_exception, SMTPSenderRefused):
                error_message = "El servidor SMTP rechazó la dirección del remitente."
                print(f"Detalles del error SMTPSenderRefused: {smtp_exception}")
            elif isinstance(smtp_exception, SMTPRecipientsRefused):
                error_message = "El servidor SMTP rechazó una o más direcciones de correo electrónico de los destinatarios."
                print(f"Detalles del error SMTPRecipientsRefused: {smtp_exception}")
            elif isinstance(smtp_exception, ConnectionError):
                error_message = "Error de conexión al intentar conectar con el servidor SMTP."
                print(f"Detalles del error ConnectionError: {smtp_exception}")
            else:
                error_message = "Error al enviar el correo electrónico."
                print(f"Detalles del error desconocido: {smtp_exception}")

            return render(request, "accounts/signUp.html", {"errorMessage": error_message})

    return render(request, "accounts/signUp.html")

def authenticateUser(request):
    username = request.GET.get("username")
    print(f"Username: {username}")
    token = request.GET.get("token")
    print(f"Token: {token}")

    try:
        user = User.objects.get(username=username)
        client = Client.objects.get(user=user)
        if client.token == token:
            client.user.is_active=True
            client.user.save()
            login(request, user)
            return redirect(index)            
        else:
            raise Http404("El usuario que estás intentando autentificar no existe")    

    except User.DoesNotExist:
        raise Http404("El usuario que estás intentando autentificar no existe")
    except Client.DoesNotExist:
        raise Http404("No se ha podido autentificar tu direccion de correo electrónico")
