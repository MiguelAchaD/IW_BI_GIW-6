from django import template

register = template.Library()

@register.simple_tag(name="get_product_URI")
def get_product_URI(product):
    # Obtiene la ruta del GIF asociado al tipo de producto
    return product.type.gif_path if product.type else None

@register.filter(name="get_generations")
def get_generations(products):
    generations = {}
    for product in products:
        prod_type = product.type.id if product.type else None
        if prod_type not in generations:
            generations[prod_type] = {}
        # Generación basada en el ID del producto, ajusta esto según sea necesario
        prod_gen = product.id.split("-")[1]
        if prod_gen not in generations[prod_type]:
            generations[prod_type][prod_gen] = []
        generations[prod_type][prod_gen].append(product)
    return generations

@register.filter(name="get_prodGenerations")
def get_prodGenerations(product_type, generations):
    return generations.get(product_type, {})

@register.filter(name="get_genToProds")
def get_genToProds(gens, gen):
    return gens.get(gen, [])

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
    return product.type.id if product.type else None

@register.filter(name="get_range")
def get_range(value):
    return range(value)

@register.filter(name="get_id")
def get_id(value):
    return value.replace(' ', '_')
