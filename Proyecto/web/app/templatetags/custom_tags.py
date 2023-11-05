from django import template

register = template.Library()

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
    prodToGen = {"phone" : "PN", "tablet" : "TB", "laptop" : "LP"}
    return generations[prodToGen[product]]

@register.filter(name="get_genToProds")
def get_genToProds(gens, gen):
    return gens[gen]

@register.filter(name="formatDec")
def formatDec(dec):
    parts = str(dec).split(".")
    decimalPart = parts[len(parts)-1]
    if (decimalPart == "00"):
        return parts[0]
    elif (decimalPart[1] == "0"):
        return str(dec)[:len(str(dec))-1]
    else:
        return str(dec)

@register.filter(name='get_range')
def get_range(value):
    return range(value)
