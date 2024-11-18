from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db import models
from datetime import date


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
    profile = models.CharField(max_length=255, default="images/profiles/default.jpg")
    creditCard = models.CharField(max_length=50, null=True)
    token = models.CharField(max_length=20, null=True)

User._meta.get_field("email")._unique = True

class Module(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    pairs = models.PositiveIntegerField(default=0)
    x = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    y = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    z = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    media_path = models.CharField(max_length=255, default="images/modules/default.png")

class Type(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)
    gif_path = models.CharField(max_length=255, default="images/products/defult.gif")
    x_svg_path = models.CharField(max_length=255, default="images/products/defult.png")
    y_svg_path = models.CharField(max_length=255, default="images/products/defult.png")
    z_svg_path = models.CharField(max_length=255, default="images/products/defult.png")

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    x = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    y = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    z = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    media_path = models.CharField(max_length=255, default="images/products/defult.png")
    color = models.CharField(max_length=255, default="blue")

class compatibleModules(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)

class CartProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    modules = models.ManyToManyField(Module)
    quantity = models.PositiveIntegerField(default=1)
    
    def delete(self, *args, **kwargs):
        self.modules.clear()
        super(CartProduct, self).delete(*args, **kwargs)

class CartRelation(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=False)
    cartProduct = models.OneToOneField(CartProduct, on_delete=models.CASCADE, null=True)

class selectedModules(models.Model):
    cartProduct = models.OneToOneField(CartProduct, on_delete=models.CASCADE, null=True)
    modules = models.ManyToManyField(Module)

class Purchase(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    date = models.DateField(default=date.today)
    modulesForProducts = models.ManyToManyField(selectedModules)