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



def isUserAuthenticated(user):
    return user.is_authenticated

def home(request):
    if request.method == "GET":
        products = {
            'phones': Product.objects.filter(id__startswith='PN'),
            'tablets': Product.objects.filter(id__startswith='TB'),
            'laptops': Product.objects.filter(id__startswith='LP')
        }

        return render(request, "home.html", {'products': products})

    if request.method == "POST":
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
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
    
    products_of_same_type = Product.objects.filter(type=product_type)
    
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
def productSelect(request, id=None):
    if request.method == 'GET':
        if (id != None):
            return redirect('modelSelect_specific', id=id)
        retrievedProducts = Product.objects.all()
        checked_ids = []
        products = []
        for product in retrievedProducts:
            product_id = str(str(product.id).split("-")[0])
            if (product_id not in checked_ids):
                product.id = product_id
                products.append(product)
                checked_ids.append(product_id)
        return render(request, "finalBuild/deviceSelection.html", {"products" : products})

@user_passes_test(isUserAuthenticated, login_url="logIn")
def modelSelect(request, id=None):
    if request.method == 'GET':
        if (id == None):
            return JsonResponse({"error": "Invalid data"}, status=400)
        productModels = Product.objects.all()
        models = []
        for product in productModels:
            product_id = str(str(product.id).split("-")[0])
            if product_id == id:
                models.append(product)
        return render(request, "finalBuild/modelSelection.html", {"models": models})

@user_passes_test(isUserAuthenticated, login_url="logIn")
def modelSelectSpecific(request, id=None):
    if request.method == 'GET':
        return redirect('finalBuild', id=id)

@user_passes_test(isUserAuthenticated, login_url="logIn")
def finalBuild(request, id=None, modules=None, color=None):
    if request.method == 'GET':
        if (id == None):
            return JsonResponse({"error": "Invalid data"}, status=400)
        
        try:
            products_retreive = Product.objects.all()
            isRealProduct = False
            for product_iteration in list(products_retreive):
                if product_iteration.id == id:
                    product = product_iteration
                    isRealProduct = True
            if not isRealProduct:
                raise Exception
        except Exception:
            return JsonResponse({"error": "Invalid data"}, status=400)
        modules_retreive = compatibleModules.objects.get(product=product)
        print(modules_retreive)
        # TODO: ...
        if (modules != None and type(modules)==list):
            try:
                modules_retreive = compatibleModules.objects.get(product=product).modules.all()
                #TODO: verify models with the product specific compatible modules
                
                #
                for module in modules:
                    if (module not in modules_retreive):
                        raise Exception
            except Exception:
                return JsonResponse({"error": "Invalid data"}, status=400)
            addToCart(request, product.id, modules)
            return render(request, "cart.html")
        return render(request, "finalBuild/build.html", {"product" : product})
    #allCompatibleModules = compatibleModules.objects.all()
#
    #products = {}
    #for obj in allCompatibleModules:
    #    product_id = str(obj.product.id).split("-")[0]
    #    if product_id in products:
    #        products[product_id].append([obj.product.id, obj.product.name, int(obj.product.price),
    #                                    int(obj.product.x), int(obj.product.y), int(obj.product.z)])
    #    else:
    #        products[product_id] = [[obj.product.id, obj.product.name, int(obj.product.price),
    #                                int(obj.product.x), int(obj.product.y), int(obj.product.z)]]
#
    #modules = {}
    #for obj in allCompatibleModules:
    #    mods = []
    #    for module in obj.modules.all():
    #        mods.append([module.id, module.name, module.price,
    #                    module.x, module.y, module.z, module.pairs])
    #    modules[obj.product.id] = mods
#
    #if request.method == "GET":
    #    return render(request, "finalBuild/build.html", {"products": products})
    #elif request.method == "POST":
    #    moduleData = request.POST.get('datos', None)
    #    cartData = request.POST.getlist('datos[]')
    #    if moduleData and moduleData.split("_")[0] == "modulesFor":
    #        response_data = modules.get(moduleData.split("_")[1], [])
    #        return JsonResponse(response_data, safe=False)
    #    elif cartData and len(list(cartData)) > 2:
    #        return addToCart(request, cartData[1], cartData[2:])
    #    else:
    #        return JsonResponse({"error": "Invalid data"}, status=400)
    #else:
    #    return JsonResponse({"error": "Method not allowed"}, status=405)

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

        module_ids = sorted([int(module_id.split("-")[0]) for module_id in modules])

        existing_cart_product = None
        for cart_product in CartProduct.objects.filter(product=product, cartrelation__client=client):
            if sorted([module.id for module in cart_product.modules.all()]) == module_ids:
                existing_cart_product = cart_product
                break

        if existing_cart_product:
            existing_cart_product.quantity += 1
            existing_cart_product.save()
        else:
            with transaction.atomic():
                new_cart_product = CartProduct.objects.create(product=product)
                new_cart_product.modules.set(module_ids)
                CartRelation.objects.create(client=client, cartProduct=new_cart_product)

        return JsonResponse("success", safe=False)
    else:
        return JsonResponse("failure", safe="False")

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