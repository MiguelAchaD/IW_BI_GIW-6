from django.db import models
from django.contrib.auth.models import User

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

class Module(models.Model):
    name = models.CharField(max_length=20)
    id = models.CharField(max_length=20, primary_key=True)
    price = models.PositiveSmallIntegerField()

class Product(models.Model):
    name = models.CharField(max_length=20)
    model = models.CharField(max_length=10)
    id = models.CharField(max_length=20, primary_key=True)
    price = models.PositiveSmallIntegerField()
    compatibleModules = models.ManyToManyField(Module)

class selectedModules(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)

class Purchase(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product)
    modulesForProducts = models.ManyToManyField(selectedModules)
    user = models.OneToOneField(User, on_delete=models.CASCADE)