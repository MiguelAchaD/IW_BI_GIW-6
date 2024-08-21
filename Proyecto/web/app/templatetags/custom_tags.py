from django import template

register = template.Library()

GENERATIONS = {
        "phone" : "PN",
        "tablet" : "TB",
        "laptop" : "LP"
    }

URIS = {
        "phone" : "images/products/phone.gif",
        "tablet" : "images/products/tablet.gif",
        "laptop" : "images/products/laptop.gif"
    }

@register.tag(name="get_product_URI")
def get_product_URI(product):
    return URIS.get(product, None)

@register.filter(name="get_generations")
def get_generations(products):
    generations = {}
    for product in products:
        parts = product.model.split("-")
        prod = parts[0]
        if (prod not in generations):
            generations[prod] = {}
        prod_gen = parts[2]
        if (prod_gen not in generations[prod]):
            generations[prod][prod_gen] = []
        prod_type = parts[1]
        if (prod_type not in generations[prod][prod_gen]):
            generations[prod][prod_gen].append(product)
    return generations

@register.filter(name="get_prodGenerations")
def get_prodGenerations(product, generations):
    return generations[GENERATIONS[product]]

@register.filter(name="get_genToProds")
def get_genToProds(gens, gen):
    return gens[gen]

@register.filter(name="formatDec")
def formatDec(dec):
    parts = str(dec).split(".")
    decimalPart = parts[len(parts)-1] if len(parts) > 1 else None
    if decimalPart is None or decimalPart == "00":
        return parts[0]
    elif len(decimalPart) > 1 and decimalPart[1] == "0":
        return str(dec)[:len(str(dec))-1]
    else:
        return str(dec)

@register.filter(name="get_productType")
def get_productType(product):
    return product.model.split("-")[0]

@register.filter(name="get_range")
def get_range(value):
    return range(value)

@register.filter(name="get_listFromCM")
def get_listFromCM(object):
    result = []
    for element in object:
        modules = []
        for module in element.modules.all():
            modules.append([module.id, module.name, float(str(module.price))])
        result.append([element.product.id, element.product.name, float(str(element.product.price)), modules])
    return result