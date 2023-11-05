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

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creditCard = models.CharField(max_length=50, null=True)
    token = models.CharField(max_length=20, null=True)

User._meta.get_field("email")._unique = True

class Module(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dimensionX = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    dimensionY = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    dimensionZ = models.DecimalField(default=0, decimal_places=2, max_digits=10)

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    model = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dimensionX = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    dimensionY = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    dimensionZ = models.DecimalField(default=0, decimal_places=2, max_digits=10)

class compatibleModules(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)

class CartProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)

class CartRelation(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=False)
    cartProduct = models.ForeignKey(CartProduct, on_delete=models.DO_NOTHING, null=False)

class selectedModules(models.Model):
    cartProduct = models.OneToOneField(CartProduct, on_delete=models.CASCADE, null=True)
    modules = models.ManyToManyField(Module)

class Purchase(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    date = models.DateField()
    modulesForProducts = models.ManyToManyField(selectedModules)


 
    
#related_name: Si un modelo tiene una foreign key, el modelo asociado a esa foreign key podrá accceder a los modelos asociados mediante el nombre puesto como related_name