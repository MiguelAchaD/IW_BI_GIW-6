from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Client, CartRelation, CartProduct, Product, Type
from app.templatetags.custom_tags import *
from app.models import Product, compatibleModules
from django.http import JsonResponse
from django.db import transaction
import random
from django.core.exceptions import ImproperlyConfigured
from .models import (
    Product,
    Module,
    Client,
    CartProduct,
    CartRelation,
)



def isUserAuthenticated(user):
    return user.is_authenticated

def home(request):
    if request.method == "GET":
        types = Type.objects.all()

        available_colors = list(Product.objects.values_list('color', flat=True).distinct())

        if not available_colors or len(available_colors) < types.count():
            raise ImproperlyConfigured(
                "No hay suficientes colores únicos disponibles para asignar a cada tipo. "
                f"Se requieren al menos {types.count()} colores, pero solo hay {len(available_colors)} disponibles."
            )

        random.shuffle(available_colors)

        type_color_mapping = {type_obj.id: color for type_obj, color in zip(types, available_colors)}

        products = {}
        for type_obj in types:
            key = type_obj.name.lower()
            assigned_color = type_color_mapping[type_obj.id]
            products[key] = Product.objects.filter(type=type_obj, color=assigned_color)

        context = {
            'products': products,
        }

        print(products)

        return render(request, "home.html", context)

    elif request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        client = user.client
        client.save()

        return redirect("home")



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
                return redirect("home")
        else:
            return render(request, "accounts/logIn.html", {"errorMessage": "Credenciales inválidas"})


def logOut(request):
    logout(request)
    return redirect("home")


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
                return redirect(home)
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
        totalPrice, cartProducts = calcTotalPrice(client)
        return render(request, "cart.html", {"cartProducts": cartProducts, "totalPrice": totalPrice})

@user_passes_test(isUserAuthenticated, login_url="logIn")
def products(request, id):
    product_type = None
    
    try:
        product = Product.objects.get(id=id)
        product_type = product.type
    except Product.DoesNotExist:
        product_type = get_object_or_404(Type, id=id)
    
    products_of_same_type = Product.objects.filter(type=product_type, color="blue")
    
    return render(request, "products.html", {
        "type": product_type,
        "products": products_of_same_type
    })

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
def productSelect(request):
    if request.method == 'GET':
        retrievedProducts = Product.objects.filter(name="Medium", color="black")[::-1]
        return render(request, "finalBuild/deviceSelection.html", {"products" : retrievedProducts})

@user_passes_test(isUserAuthenticated, login_url="logIn")
def modelSelect(request, id=None):
    if request.method == 'GET':
        if (id == None):
            return JsonResponse({"error": "Invalid data"}, status=400)
        
        product = Product.objects.get(id=id)
        models = Product.objects.filter(type_id=product.type_id, color="black")
        return render(request, "finalBuild/modelSelection.html", {"product": product, "models": models})

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from .models import Product, compatibleModules

@user_passes_test(isUserAuthenticated, login_url="logIn")
def finalBuild(request, product_id=None, modules=None, color=None):
    if request.method == 'GET':
        if not product_id:
            return JsonResponse({"error": "Invalid data"}, status=400)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product does not exist"}, status=400)
        
        try:
            modules_retrieve = compatibleModules.objects.get(product=product).modules.all()
        except compatibleModules.DoesNotExist:
            modules_retrieve = None 
        
        context = {
            "product": product,
            "modules": modules_retrieve
        }
        return render(request, "finalBuild/build.html", context)
    
    elif request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        client = user.client
        client.save()

        return redirect("home")


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

@csrf_exempt
def addToCart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            module_ids = data.get('modules', [])
            color = data.get("color")

            if not product_id or not color:
                return JsonResponse({"error": "Product ID and color are required."}, status=400)

            client = Client.objects.get(user=request.user)

            try:
                base_product = Product.objects.get(id=product_id)
                product_type = base_product.type
                product_name = base_product.name
            except Product.DoesNotExist:
                return JsonResponse({"error": "Product does not exist."}, status=404)

            try:
                product = Product.objects.get(
                    type=product_type,
                    name=product_name,
                    color=color
                )
            except Product.DoesNotExist:
                return JsonResponse({"error": f"No product found with name '{product_name}', type '{product_type}', and color '{color}'."}, status=404)

            valid_module_ids = []
            for module_id in module_ids:
                try:
                    Module.objects.get(id=str(module_id))
                    valid_module_ids.append(str(module_id))
                except Module.DoesNotExist:
                    return JsonResponse({"error": f"Module with ID '{module_id}' does not exist."}, status=404)

            sorted_module_ids = sorted(valid_module_ids)

            existing_cart_product = None
            cart_products = CartProduct.objects.filter(product=product, cartrelation__client=client).prefetch_related('modules')

            for cart_product in cart_products:
                cart_product_module_ids = sorted([module.id for module in cart_product.modules.all()])
                if cart_product_module_ids == sorted_module_ids:
                    existing_cart_product = cart_product
                    break

            if existing_cart_product:
                existing_cart_product.quantity += 1
                existing_cart_product.save()
                return JsonResponse({"message": "Product quantity updated in cart."}, status=200)
            else:
                with transaction.atomic():
                    new_cart_product = CartProduct.objects.create(product=product)
                    modules_queryset = Module.objects.filter(id__in=valid_module_ids)
                    new_cart_product.modules.set(modules_queryset)
                    new_cart_product.save()

                    CartRelation.objects.create(client=client, cartProduct=new_cart_product)

                return JsonResponse({"message": "Product added to cart."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Associated data does not exist."}, status=400)
        except Exception as e:
            print(f"Error in addToCart: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
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