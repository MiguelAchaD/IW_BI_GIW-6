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
        client = Client.objects.get(user=request.user)
        totalPrice, cartProducts = calcTotalPrice(client)
        return render(request, "cart.html", {"cartProducts": cartProducts, "totalPrice": totalPrice})

def calcTotalPrice(client):
    cartRelations = CartRelation.objects.filter(client=client)
    if cartRelations.count() > 0:
        cartProducts = CartProduct.objects.filter(cartrelation__in=cartRelations)
        if cartProducts.count() > 0:
            totalPrice = 0
            for cartProduct in cartProducts:
                for module in cartProduct.modules.all():
                    totalPrice += module.price * cartProduct.quantity
                totalPrice += cartProduct.product.price * cartProduct.quantity
            return totalPrice, cartProducts
    return -1, []

def updateQuantity(request, cartProductId, change):
    if request.method == "GET":
        try:
            cart_Product = CartProduct.objects.get(id=cartProductId)
            cart_Product.quantity += int(change)
            quantity = cart_Product.quantity
            if cart_Product.quantity <= 0:
                cart_Product.delete()
            else:
                cart_Product.save()
            client = Client.objects.get(user=request.user)
            totalPrice, _ = calcTotalPrice(client)
            if(totalPrice >= 0):
                return JsonResponse({'status': 'success', 'newTotalPrice': totalPrice, 'newQuantity': quantity})
            return JsonResponse({'status': 'empty'})
        except CartProduct.DoesNotExist as e:
            return JsonResponse({'status': 'error', 'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Error eliminando el producto del carrito'}, status=500)

def removeFromCart(request, cartProductId):
    if request.method == "GET":
        try:
            cart_product = CartProduct.objects.get(id=cartProductId)
            cart_product.delete()
            client = Client.objects.get(user=request.user)
            totalPrice, _ = calcTotalPrice(client)
            if(totalPrice >= 0):
                return JsonResponse({'status': 'success', 'newTotalPrice': totalPrice})
            return JsonResponse({'status': 'empty'})
        except CartProduct.DoesNotExist as e:
            print("ERROR: " + str(e))
            return JsonResponse({'status': 'error', 'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            print("ERROR: " + str(e))
            return JsonResponse({'status': 'error', 'message': 'Error eliminando el producto del carrito'}, status=500)

def addToCart(request, product_id, modules):
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)

        # Convertir IDs de módulos a enteros y ordenarlos para la comparación
        module_ids = sorted([int(module_id.split("-")[0]) for module_id in modules])

        # Buscar un CartProduct existente con el mismo producto y módulos
        existing_cart_product = None
        for cart_product in CartProduct.objects.filter(product=product, cartrelation__client=client):
            if sorted([module.id for module in cart_product.modules.all()]) == module_ids:
                existing_cart_product = cart_product
                break

        # Si existe, incrementar la cantidad
        if existing_cart_product:
            existing_cart_product.quantity += 1
            existing_cart_product.save()
        else:
            # Si no existe, crear uno nuevo
            with transaction.atomic():
                new_cart_product = CartProduct.objects.create(product=product)
                new_cart_product.modules.set(module_ids)
                CartRelation.objects.create(client=client, cartProduct=new_cart_product)

        return JsonResponse("success", safe=False)
    else:
        return JsonResponse("failure", safe="False")

        
@user_passes_test(isUserAuthenticated, login_url="logIn")
def products(request, product):
    products = ["phone", "tablet", "laptop"]
    generations = get_generations(Product.objects.all())
    product_generations = get_prodGenerations(product, generations)
    if product in products:
        product = product.capitalize()
        productURI = Product.objects.get(name=product).image
        return render(request, "products/products.html", {'product_generations': product_generations, 'productURI' : productURI})
    raise Http404("Error cargando los productos")


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