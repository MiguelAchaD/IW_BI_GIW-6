from django.db import models

# Create your models here.

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

class Client(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    username = models.CharField(max_length=20, primary_key=True)
    birthDate = models.DateField()
    mail = models.CharField(max_length=40)
    creditCard = models.CharField(max_length=50)

class selectedModules(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)

class Purchase(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product)
    modulesForProducts = models.ManyToManyField(selectedModules)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)



