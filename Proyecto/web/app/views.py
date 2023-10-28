from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

def index(request):
    return render(request, "index.html")

def logIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "accounts/logIn.html", {"errorMessage": "Credenciales inválidas"})

    return render(request, "accounts/logIn.html")

def signUp(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirmPassword"]

        if not email.endswith("@gmail.com"):
            return render(request, "accounts/signUp.html", {"errorMessage": "El correo electrónico debe ser de dominio @gmail.com"})

        if password != confirm_password:
            return render(request, "accounts/signUp.html", {"errorMessage": "Las contraseñas no coinciden"})

    
        # TODO revisar esto
        user = User.objects.create_user(email=email, password=password)
        token = get_random_string(length=20)
        user.client.token = token
        user.client.save()
        #
        
        send_mail(
            "Autenticación de Correo Electrónico", 
            f"Haz clic en el siguiente enlace para autenticar tu correo electrónico: http://tu-sitio.com/autenticar/{token}/", 
            "noreply@tu-sitio.com", 
            [email],
            fail_silently=False
        )

        # TODO - Redirigir a una página de confirmación
        return render(request, "accounts/email_confirmation.html", {"email": email})

    return render(request, "accounts/signUp.html")


