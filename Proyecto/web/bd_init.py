import faker
from django.utils.crypto import get_random_string
from app.models import *
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

django.setup()

fake = faker.Faker()


def initUser():
    name = fake.first_name()
    lastName = fake.last_name()
    username = str(name).lower() + lastName
    email = username + "@gmail.com"
    password = get_random_string(length=10)
    is_active = False
    is_staff = False
    is_superuser = False
    return User(username=username, password=password, email=email, first_name=name, last_name=lastName, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)


def initClients():
    token = get_random_string(length=20)
    user = initUser()
    user.save()
    creditCard = fake.credit_card_full(card_type="mastercard")
    return Client(token=token, user=user, creditCard=creditCard)


def main():
    '''
    # Random Clients Creation
    for _ in range(20):
        client = initClients()
        client.save()
    print(Client.objects.all())
    '''
    
    # Modules Creation
    modules = {
        "Charger lightning 20W" : [20, 1],
        "Charger lightning 20W Data-transmition" : [30, 1],
        "Charger lightning 25W Data-transmition" : [40, 1],
        "Charger lightning 40W" : [40, 1],
        "Charger lightning 40W Data-transmition" : [45, 1],
        "Charger lightning 45W Data-transmition" : [50, 1],
        "Charger lightning 90W" : [50, 1],
        "Charger lightning 90W Data-transmition" : [60, 1],
        "Charger lightning 95W Data-transmition" : [70, 1],
        'Screen 14" 16:9 fullHD LED': [53, 2],
        'Screen 16" 16:9 UHD OLED': [90, 2],
        'Screen 19" 16:9 4K QLED': [130, 2],
        "Dock USB2.0 miniHDMI ChargePort": [20, 3],
        "Dock USB3.0 HDMI ChargePort": [30, 3],
        "Dock USB3.0 USB4.0 HDMI DisplayPort ChargePort": [40, 3],
        "Keyboard es_ES": [10, 4],
        "Keyboard en_US": [10, 4],
        'Screen 6.1" fullHD': [70, 2],
        'Screen 6.7" 2k': [120, 2],
        'Screen 7.2" 2K': [135, 2],
        'Screen 9.5" fullHD': [40, 2],
        'Screen 10.9" 2k': [45, 2],
        'Screen 11" 4K': [50, 2],
        "Camera 10MP": [40, 5],
        "Camera 12MP": [45, 5],
        "Camera 14MP": [60, 5],
    }

    for element in modules:
        Module(name=element, price=modules[element]
               [0], pairs=modules[element][1]).save()
    # Products Creation
    plpmn = Product(id="LP-000", name="Laptop Mini", model="LP-Mn-0",
                    price=100, dimensionX=277, dimensionY=219, dimensionZ=9)
    plpmn.save()
    cm = compatibleModules(product=plpmn)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 90W'), Module.objects.get(name='Charger lightning 90W Data-transmition'), Module.objects.get(name='Screen 14" 16:9 fullHD LED'), Module.objects.get(name="Dock USB2.0 miniHDMI ChargePort"), Module.objects.get(
        name="Keyboard es_ES"), Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()

    plp = Product(id="LP-001", name="Laptop", model="LP-Nm-0",
                  price=120, dimensionX=348, dimensionY=243, dimensionZ=9)
    plp.save()
    cm = compatibleModules(product=plp)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 90W Data-transmition'), Module.objects.get(name='Screen 16" 16:9 UHD OLED'), Module.objects.get(name="Dock USB3.0 HDMI ChargePort"), Module.objects.get(name="Keyboard es_ES"),
                   Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()

    plpmx = Product(id="LP-002", name="Laptop Max", model="LP-Mx-0",
                    price=130, dimensionX=392, dimensionY=259, dimensionZ=9)
    plpmx.save()
    cm = compatibleModules(product=plpmx)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 90W Data-transmition'), Module.objects.get(name='Charger lightning 95W Data-transmition'), Module.objects.get(name='Screen 16" 16:9 UHD OLED'), Module.objects.get(name="Dock USB3.0 HDMI ChargePort"), Module.objects.get(name="Dock USB3.0 USB4.0 HDMI DisplayPort ChargePort"), Module.objects.get(
        name="Keyboard es_ES"), Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()

    tbmn = Product(id="TB-000", name="Tablet Mini", model="TB-Mn-0",
                   price=130, dimensionX=135, dimensionY=200, dimensionZ=8.4)
    tbmn.save()
    cm = compatibleModules(product=tbmn)
    cm.save()
    cm.modules.add(Module.objects.get(Module.objects.get(name='Charger lightning 40W'), Module.objects.get(name='Charger lightning 40W Data-transmition'), name='Screen 9.5" fullHD'), Module.objects.get(
        name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()

    tb = Product(id="TB-001", name="Tablet", model="TB-Nm-0",
                 price=150, dimensionX=170, dimensionY=239, dimensionZ=8.4)
    tb.save()
    cm = compatibleModules(product=tb)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 40W Data-transmition'), Module.objects.get(name='Screen 10.9" 2k'),
                   Module.objects.get(name="Camera 12MP"))
    cm.save()

    tbmx = Product(id="TB-002", name="Tablet Max", model="TB-Mx-0",
                   price=160, dimensionX=186, dimensionY=241, dimensionZ=8.4)
    tbmx.save()
    cm = compatibleModules(product=tbmx)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 40W Data-transmition'), Module.objects.get(name='Charger lightning 45W Data-transmition'), Module.objects.get(name='Screen 11" 4K'), Module.objects.get(
        name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()

    pnmn = Product(id="PN-000", name="Phone Mini", model="PN-Mn-0",
                   price=130, dimensionX=64.2, dimensionY=131, dimensionZ=7.4)
    pnmn.save()
    cm = compatibleModules(product=pnmn)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 20W'), Module.objects.get(name='Charger lightning 20W Data-transmition'), Module.objects.get(name='Screen 6.1" fullHD'), Module.objects.get(
        name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()

    pn = Product(id="PN-001", name="Phone", model="PN-Nm-0",
                 price=140, dimensionX=71.5, dimensionY=147, dimensionZ=7.4)
    pn.save()
    cm = compatibleModules(product=pn)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 20W Data-transmition'), Module.objects.get(name='Screen 6.7" 2k'),
                   Module.objects.get(name="Camera 12MP"))
    cm.save()

    pnmx = Product(id="PN-002", name="Phone Max", model="PN-Mx-0",
                   price=150, dimensionX=78.1, dimensionY=161, dimensionZ=7.4)
    pnmx.save()
    cm = compatibleModules(product=pnmx)
    cm.save()
    cm.modules.add(Module.objects.get(name='Charger lightning 20W Data-transmition'), Module.objects.get(name='Charger lightning 25W Data-transmition'), Module.objects.get(name='Screen 7.2" 4K'), Module.objects.get(
        name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()
    


if __name__ == "__main__":
    main()
