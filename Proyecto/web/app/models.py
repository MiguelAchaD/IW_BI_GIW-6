from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.

class Client(models.Model):
    id = models.CharField(max_length=20, default=get_random_string(length=20), primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    birthDate = models.DateField()
    email = models.EmailField(max_length=40, null=True)
    creditCard = models.CharField(max_length=50, null=True)

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
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
"""