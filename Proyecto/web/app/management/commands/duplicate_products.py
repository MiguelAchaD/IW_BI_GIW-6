# your_app/management/commands/duplicate_products.py

from django.core.management.base import BaseCommand
from app.models import Product, Type  # Reemplaza 'your_app' con el nombre de tu aplicación
import os
import re

class Command(BaseCommand):
    help = 'Duplica productos existentes con nuevos colores (red y black) asignando IDs incrementales.'

    def handle(self, *args, **options):
        # Define los nuevos colores
        new_colors = ['red', 'black']

        # Obtén todos los tipos de productos
        types = Type.objects.all()

        # Patrón para extraer el número del ID (asumiendo formato PREFIX-NUMBER)
        id_pattern = re.compile(r'^(?P<prefix>[A-Z]+)-(?P<number>\d+)$')

        # Diccionario para almacenar el siguiente número por tipo
        next_number = {}

        # Inicializar el siguiente número para cada tipo
        for type_obj in types:
            # Filtrar productos por tipo y extraer los números
            type_products = Product.objects.filter(type=type_obj)
            max_num = 0
            for product in type_products:
                match = id_pattern.match(product.id)
                if match:
                    num = int(match.group('number'))
                    if num > max_num:
                        max_num = num
            # El siguiente número será max_num + 1
            next_number[type_obj.id] = max_num + 1

        # Contador para seguimiento
        total_duplicates = 0

        # Iterar sobre cada tipo y duplicar productos
        for type_obj in types:
            type_prefix = type_obj.id
            type_products = Product.objects.filter(type=type_obj)
            for product in type_products:
                for color in new_colors:
                    # Asignar el siguiente ID
                    new_num = next_number[type_obj.id]
                    new_id = f"{type_prefix}-{new_num:03d}"  # Formato con ceros a la izquierda, e.g., LP-003

                    # Verificar si el nuevo ID ya existe
                    if Product.objects.filter(id=new_id).exists():
                        self.stdout.write(self.style.WARNING(f"Ya existe el ID: {new_id}, omitiendo."))
                        next_number[type_obj.id] += 1
                        continue

                    # Definir la nueva ruta de media_path
                    new_media_path = self.update_media_path(product.media_path, color)

                    # Crear la nueva instancia de Product
                    new_product = Product(
                        id=new_id,
                        name=product.name,
                        price=product.price,
                        media_path=new_media_path,
                        x=product.x,
                        y=product.y,
                        z=product.z,
                        type=product.type,
                        color=color
                    )

                    try:
                        # Guardar el nuevo producto en la base de datos
                        new_product.save()
                        total_duplicates += 1
                        self.stdout.write(self.style.SUCCESS(f"Duplicado: {product.id} -> {new_id} (Color: {color})"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al duplicar {product.id} -> {new_id}: {str(e)}"))

                    # Incrementar el siguiente número para este tipo
                    next_number[type_obj.id] += 1

        self.stdout.write(self.style.SUCCESS(f"Total de productos duplicados: {total_duplicates}"))

    def update_media_path(self, original_path, new_color):
        """
        Actualiza la ruta de media_path reemplazando el color existente con el nuevo color.
        Asume que el color está presente en el nombre del archivo antes de la extensión.
        Ejemplo: laptop.mini.blue.png -> laptop.mini.red.png
        """
        # Separar la ruta y el nombre del archivo
        directory, filename = os.path.split(original_path)
        # Separar el nombre del archivo y la extensión
        name, ext = os.path.splitext(filename)
        # Dividir el nombre por puntos
        parts = name.split('.')

        # Reemplazar el último segmento si es un color conocido
        if parts[-1] in ['blue', 'red', 'black']:
            parts[-1] = new_color
        else:
            # Si no hay un color al final, agregar el nuevo color
            parts.append(new_color)

        # Reconstruir el nombre del archivo
        new_filename = '.'.join(parts) + ext

        # Reconstruir la ruta completa
        new_media_path = os.path.join(directory, new_filename)

        return new_media_path
