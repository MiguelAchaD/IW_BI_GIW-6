from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

"""
    Campos de User
    username: Nombre de usuario único utilizado para la autenticación.
    password: Contraseña del usuario (almacenada de forma segura mediante hash).
    email: Dirección de correo electrónico del usuario (opcionalmente única).
    first_name: Primer nombre del usuario.
    last_name: Apellido del usuario.
    is_active: Booleano que indica si la cuenta del usuario está activa.
    is_staff: Booleano que indica si el usuario tiene acceso al sitio de administración.
    is_superuser: Booleano que indica si el usuario tiene todos los permisos sin restricciones.
"""

class Client(models.Model):
    # TODO: Una vez esté creada la funcionalidad de registro (registrar auth_user, y linkearlo al cliente como fk), este debe de ser "null=False"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #
    birthDate = models.DateField()
    creditCard = models.CharField(max_length=50, null=True)

class Module(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveSmallIntegerField()

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    model = models.CharField(max_length=10)
    price = models.PositiveSmallIntegerField()
    compatibleModules = models.ManyToManyField(Module)

class selectedModules(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True)
    modules = models.ManyToManyField(Module)

class Purchase(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField()
    modulesForProducts = models.ManyToManyField(selectedModules)