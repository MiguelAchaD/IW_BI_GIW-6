import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
import django
django.setup()
from app.models import *
from django.utils.crypto import get_random_string
import faker

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
    modules = {"Battery 11560mAh 11.55v" : [0, 1],
               "Battery 12560mAh 11.55v" : [0, 1],
               "Battery 14560mAh 11.55v" : [0, 1],
               'Screen 14" 16:9 fullHD LED' : [0, 2],
               'Screen 16" 16:9 UHD OLED' : [0, 2],
               'Screen 19" 16:9 4K QLED' : [0, 2],
               "Dock USB2.0 miniHDMI ChargePort" : [0, 3],
               "Dock USB3.0 HDMI ChargePort" : [0, 3],
               "Dock USB3.0 USB4.0 HDMI DisplayPort ChargePort" : [0, 3],
               "Keyboard es_ES" : [0, 4],
               "Keyboard en_US" : [0, 4],
               "Battery 3095mAh 3.6v" : [0, 1],
               "Battery 4323mAh 3.6v" : [0, 1],
               "Battery 4422mAh 3.6v" : [0, 1],
               'Screen 6.1" fullHD' : [0, 2],
               'Screen 6.7" 2k' : [0, 2],
               'Screen 7.2" 4K' : [0, 2],
               "Battery 4440mAh 3.6v" : [0, 1],
               "Battery 6930mAh 3.6v" : [0, 1],
               "Battery 11560mAh 3.6v" : [0, 1],
               'Screen 9.5" fullHD' : [0, 2],
               'Screen 10.9" 2k' : [0, 2],
               'Screen 11" 4K' : [0, 2],
               "Camera 10MP" : [0, 5],
               "Camera 12MP" : [0, 5],
               "Camera 14MP" : [0, 5],
               }
    
    for element in modules:
        Module(name=element, price=modules[element][0], pairs=modules[element][1]).save()
    # Products Creation
    plpmn = Product(id="LP-000", name="Laptop Mini", model="LP-Mn", price=0, dimensionX=277, dimensionY=219, dimensionZ=9)
    plpmn.save()
    cm = compatibleModules(product=plpmn)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 11560mAh 11.55v"), Module.objects.get(name='Screen 14" 16:9 fullHD LED'), Module.objects.get(name="Dock USB2.0 miniHDMI ChargePort"), Module.objects.get(name="Keyboard es_ES"), Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()
    
    plp = Product(id="LP-001", name="Laptop", model="LP", price=0, dimensionX=348, dimensionY=243, dimensionZ=9)
    plp.save()
    cm = compatibleModules(product=plp)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 12560mAh 11.55v"), Module.objects.get(name='Screen 16" 16:9 UHD OLED'), Module.objects.get(name="Dock USB3.0 HDMI ChargePort"), Module.objects.get(name="Keyboard es_ES"), Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()
    
    plpmx = Product(id="LP-002", name="Laptop Max", model="LP-Mx", price=0, dimensionX=392, dimensionY=259, dimensionZ=9)
    plpmx.save()
    cm = compatibleModules(product=plpmx)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 14560mAh 11.55v"), Module.objects.get(name='Screen 16" 16:9 UHD OLED'), Module.objects.get(name="Dock USB3.0 HDMI ChargePort"), Module.objects.get(name="Dock USB3.0 USB4.0 HDMI DisplayPort ChargePort"), Module.objects.get(name="Keyboard es_ES"), Module.objects.get(name="Keyboard en_US"), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()

    tbmn = Product(id="TB-000", name="Tablet Mini", model="TB-Mn", price=0, dimensionX=135, dimensionY=200, dimensionZ=8.4)
    tbmn.save()
    cm = compatibleModules(product=tbmn)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 4440mAh 3.6v"), Module.objects.get(name='Screen 9.5" fullHD'), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()

    tb = Product(id="TB-001", name="Tablet", model="TB", price=0, dimensionX=170, dimensionY=239, dimensionZ=8.4)
    tb.save()
    cm = compatibleModules(product=tb)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 6930mAh 3.6v"), Module.objects.get(name='Screen 10.9" 2k'), Module.objects.get(name="Camera 12MP"))
    cm.save()

    tbmx = Product(id="TB-002", name="Tablet Max", model="TB-Mx", price=0, dimensionX=186, dimensionY=241, dimensionZ=8.4)
    tbmx.save()
    cm = compatibleModules(product=tbmx)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 11560mAh 3.6v"), Module.objects.get(name='Screen 11" 4K'), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()

    pnmn = Product(id="PN-000", name="Phone Mini", model="PN-Mn", price=0, dimensionX=64.2, dimensionY=131, dimensionZ=7.4)
    pnmn.save()
    cm = compatibleModules(product=pnmn)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 3095mAh 3.6v"), Module.objects.get(name='Screen 6.1" fullHD'), Module.objects.get(name="Camera 10MP"), Module.objects.get(name="Camera 12MP"))
    cm.save()

    pn = Product(id="PN-001", name="Phone", model="PN", price=0, dimensionX=71.5, dimensionY=147, dimensionZ=7.4)
    pn.save()
    cm = compatibleModules(product=pn)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 4323mAh 3.6v"), Module.objects.get(name='Screen 6.7" 2k'), Module.objects.get(name="Camera 12MP"))
    cm.save()

    pnmx = Product(id="PN-002", name="Phone Max", model="PN-Mx", price=0, dimensionX=78.1, dimensionY=161, dimensionZ=7.4)
    pnmx.save()
    cm = compatibleModules(product=pnmx)
    cm.save()
    cm.modules.add(Module.objects.get(name="Battery 4422mAh 3.6v"), Module.objects.get(name='Screen 7.2" 4K'), Module.objects.get(name="Camera 12MP"), Module.objects.get(name="Camera 14MP"))
    cm.save()


if __name__ == "__main__":
    main()