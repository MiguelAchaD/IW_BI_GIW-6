from django.contrib.sites.requests import RequestSite
from django.core.exceptions import ImproperlyConfigured
import random
from .models import Type, Product

def assign_colors_to_types():
    """
    Asigna colores únicos a cada tipo de producto.
    """
    types = Type.objects.all()
    available_colors = list(Product.objects.values_list('color', flat=True).distinct())

    if not available_colors or len(available_colors) < types.count():
        raise ImproperlyConfigured(
            "No hay suficientes colores únicos disponibles para asignar a cada tipo. "
            f"Se requieren al menos {types.count()} colores, pero solo hay {len(available_colors)} disponibles."
        )

    random.shuffle(available_colors)

    # Asignar un color a cada tipo
    type_color_mapping = {type_obj.id: color for type_obj, color in zip(types, available_colors)}
    return type_color_mapping

def getURL(request):
    """
    Devuelve la url desde la que se hace el request
    """
    current_site = RequestSite(request)
    return f"http://{current_site.domain}"
