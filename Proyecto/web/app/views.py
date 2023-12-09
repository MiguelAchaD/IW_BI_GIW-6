import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from smtplib import SMTPException, SMTPAuthenticationError, SMTPSenderRefused, SMTPRecipientsRefused
from socket import error as ConnectionError
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from app.utils import getURL
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from .models import Client, CartRelation, CartProduct, Product, Module
from app.templatetags.custom_tags import *
from app.models import Product, compatibleModules
from django.http import JsonResponse
from django.db import transaction
from django.http import HttpResponseRedirect



def isUserAuthenticated(user):
    return user.is_authenticated


def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    if request.method == "POST":
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()

        client = user.client
        client.save()

        return redirect("index")


def logIn(request):
    if request.method == "GET":
        return render(request, "accounts/logIn.html")
    elif request.method == "POST":
        next = request.GET.get("next")

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            if next:
                return redirect(next)
            else:
                return redirect("index")
        else:
            return render(request, "accounts/logIn.html", {"errorMessage": "Credenciales inválidas"})


def logOut(request):
    logout(request)
    return redirect("index")


def signUp(request):
    if request.method == "GET":
        return render(request, "accounts/signUp.html")
    elif request.method == "POST":
        next = request.GET.get("next")

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
            existing_user = User.objects.get(email=email)
            existing_client = Client.objects.get(user=existing_user)

            if not existing_user.is_active:
                existing_user.email = email
                existing_user.set_password(password)
                existing_user.save()

                existing_client.token = token
                existing_client.save()
            else:
                return render(request, "accounts/signUp.html", {"errorMessage": "Este usuario ya está registrado. Inicia sesión con ese usuario, inicia sesión con google o utiliza otro nombre."})

        url = getURL(request)
        if url is None:
            print("Error cargando la URL del usuario")
            return render(request, "accounts/signUp.html", {"errorMessage": "Se ha producido un error cargando la URL"})

        try:
            if next:
                message = f"Haz clic en el siguiente enlace para autenticar tu correo electrónico: {url}/authenticate/newUser?email={email}&token={token}&next={next}"
            else:
                message = f"Haz clic en el siguiente enlace para autenticar tu correo electrónico: {url}/authenticate/newUser?email={email}&token={token}"
            send_mail(
                subject="Autenticación de Correo Electrónico",
                message=message,
                from_email="ecomodstechnology@gmail.com",
                recipient_list=[email],
                fail_silently=False
            )
            send_mail(
                subject="Aviso de Intento de Autenticación de Correo Electrónico",
                message=f"Se está intentando autentificar el correo '{email}' a través del token '{token}'",
                from_email="ecomodstechnology@gmail.com",
                recipient_list=["diego.merino@opendeusto.es",
                                "miguel.acha@opendeusto.es"],
                fail_silently=False
            )
            return render(request, "accounts/emailConfirmation.html", {"email": email})

        except SMTPException as smtp_exception:
            if isinstance(smtp_exception, SMTPAuthenticationError):
                error_message = "Error de autenticación SMTP."
                print(
                    f"Detalles de error de autenticación SMTP: {smtp_exception}")
            elif isinstance(smtp_exception, SMTPSenderRefused):
                error_message = "El servidor SMTP rechazó la dirección del remitente."
                print(
                    f"Detalles del error SMTPSenderRefused: {smtp_exception}")
            elif isinstance(smtp_exception, SMTPRecipientsRefused):
                error_message = "El servidor SMTP rechazó una o más direcciones de correo electrónico de los destinatarios."
                print(
                    f"Detalles del error SMTPRecipientsRefused: {smtp_exception}")
            elif isinstance(smtp_exception, ConnectionError):
                error_message = "Error de conexión al intentar conectar con el servidor SMTP."
                print(f"Detalles del error ConnectionError: {smtp_exception}")
            else:
                error_message = "Error al enviar el correo electrónico."
                print(f"Detalles del error desconocido: {smtp_exception}")

            return render(request, "accounts/signUp.html", {"errorMessage": error_message})


def authenticateUser(request):
    if request.method == "GET":
        next = request.GET.get("next")
        email = request.GET.get("email")
        token = request.GET.get("token")

        try:
            user = User.objects.get(email=email)
            client = Client.objects.get(user=user, token=token)
            client.user.is_active = True
            client.user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            if next:
                return redirect(next)
            else:
                return redirect(index)
        except User.DoesNotExist:
            raise Http404(
                "El usuario que estás intentando autentificar no existe")
        except Client.DoesNotExist:
            raise Http404(
                "No se ha podido autentificar tu dirección de correo electrónico")


@user_passes_test(isUserAuthenticated, login_url="logIn")
def viewCart(request):
    if request.method == "GET":
        client = Client.objects.get(user=request.user)
        cart_relations = CartRelation.objects.filter(client=client)
        if cart_relations.count() > 0:
            cart_Products = CartProduct.objects.filter(
                cartrelation__in=cart_relations)
            modulesPrice = 0
            
            for cart_Product in cart_Products:
                for module in cart_Product.modules.all():
                    modulesPrice += module.price
            
            if cart_Products.count() > 0:
                total_price = sum(cart_Product.product.price * cart_Product.quantity for cart_Product in cart_Products) + modulesPrice
                print("ENTRA POR AQUÍ")
                return render(request, "cart.html", {"isEmpty": False, "cart_Products": cart_Products, "total_price": total_price})
        
        return render(request, "cart.html", {"isEmpty": True})
        #return HttpResponseRedirect('/builder/')



def addToCart(request, product_id, modules):
    if request.method == 'POST':
        prodIDs = {}
        for obj in compatibleModules.objects.all():
            prodIDs[obj.product.id] = []
            for module in obj.modules.all():
                prodIDs[obj.product.id].append(module.id)
        if properCart(([product_id] + modules), prodIDs):
            client = Client.objects.get(user=request.user)
            product = Product.objects.get(id=product_id)
            mod = []
            for element in modules:
                mod.append((int(element.split("-")[0])))
            with transaction.atomic():
                cart_Product, created = CartProduct.objects.get_or_create(
                    product=product)
                cart_Product.modules.clear()
                cart_Product.modules.add(*mod)
                cart_relation, created = CartRelation.objects.get_or_create(
                    client=client, cartProduct=cart_Product)
                cart_Product.quantity += 1
            
            cart_Product.save()
            cart_relation.save()

            return JsonResponse("success", safe=False)
        else:
            return JsonResponse("failure", safe="False")


@user_passes_test(isUserAuthenticated, login_url="logIn")
def removeFromCart(request, product_id):
    if request.method == "GET":
        client = Client.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)

        cart_relation = CartRelation.objects.get(client=client)
        cart_Product = CartProduct.objects.get(
            product=product, cartrelation=cart_relation)

        cart_Product.quantity -= 1
        if cart_Product.quantity <= 0:
            cart_Product.delete()
        else:
            cart_Product.save()

        return redirect("view_cart")


@user_passes_test(isUserAuthenticated, login_url="logIn")
def products(request, product):
    products = ["phone", "tablet", "laptop"]
    print(products)
    # TODO: error en una de estas dos templatetags
    generations = get_generations(Product.objects.all())
    product_generations = get_prodGenerations(product, generations)
    if product in products:
        return render(request, "products/products.html", {"product": product, 'product_generations': product_generations})


@user_passes_test(isUserAuthenticated, login_url="logIn")
def updateProfilePicture(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        image_url = data.get('imageUrl')

        if not image_url:
            return JsonResponse({'status': 'error', 'message': 'No se proporcionó URL de imagen'}, status=400)

        client = Client.objects.get(user=request.user)
        client.profile = image_url
        client.save()

        return JsonResponse({'status': 'success', 'message': 'Imagen actualizada correctamente'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@user_passes_test(isUserAuthenticated, login_url="logIn")
def builder(request):
    allcompatibleModules = compatibleModules.objects.all()

    products = {}
    for obj in allcompatibleModules:
        product_id = str(obj.product.id).split("-")[0]
        if product_id in products:
            products[product_id].append([obj.product.id, obj.product.name, int(obj.product.price),
                                        int(obj.product.dimensionX), int(obj.product.dimensionY), int(obj.product.dimensionZ)])
        else:
            products[product_id] = [[obj.product.id, obj.product.name, int(obj.product.price),
                                    int(obj.product.dimensionX), int(obj.product.dimensionY), int(obj.product.dimensionZ)]]

    modules = {}
    for obj in allcompatibleModules:
        mods = []
        for module in obj.modules.all():
            mods.append([module.id, module.name, module.price,
                        module.dimensionX, module.dimensionY, module.dimensionZ, module.pairs])
        modules[obj.product.id] = mods

    if request.method == "GET":
        return render(request, "finalBuild/build.html", {"products": products})
    elif request.method == "POST":
        moduleData = request.POST.get('datos', None)
        cartData = request.POST.getlist('datos[]')
        if moduleData and moduleData.split("_")[0] == "modulesFor":
            response_data = modules.get(moduleData.split("_")[1], [])
            return JsonResponse(response_data, safe=False)
        elif cartData and len(list(cartData)) > 2:
            return addToCart(request, cartData[1], cartData[2:])
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    
    # elif request.method == "POST":
    #    print(datos_nuevos)
    #    return JsonResponse({'mensaje': 'Modelo actualizado correctamente'})

def properCart(cartData, prodIDs):
    proper = True
    index = 0

    while (proper == True and index < len(cartData)):
        if (index == 0):
            if ((cartData[0] in list(prodIDs.keys()))):
                proper = True
            else:
                proper = False
        else:
            if ((int(cartData[index].split("-")[0]) in list(prodIDs[cartData[0]]))):
                proper = True
            else:
                proper = False
        index += 1
    return proper