# app/management/commands/assign_compatiblemodules.py

from django.core.management.base import BaseCommand
from app.models import Product, compatibleModules
from django.db.models import Q

class Command(BaseCommand):
    help = 'Asigna módulos compatibles de productos azules a sus equivalentes de otros colores (red y black).'

    def handle(self, *args, **options):
        target_colors = ['red', 'black']
        blue_color = 'blue'
        total_assigned = 0
        total_skipped = 0
        total_errors = 0

        blue_products = Product.objects.filter(color=blue_color)

        if not blue_products.exists():
            self.stdout.write(self.style.WARNING(f"No hay productos con color '{blue_color}' para procesar."))
            return

        for blue_product in blue_products:
            try:
                blue_compatible_modules = compatibleModules.objects.get(product=blue_product).modules.all()
            except compatibleModules.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"El producto azul {blue_product.id} no tiene compatibleModules. Omitiendo."))
                total_skipped += 1
                continue

            for color in target_colors:
                try:
                    equivalent_product = Product.objects.get(
                        type=blue_product.type,
                        name=blue_product.name,
                        color=color
                    )
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"No se encontró el producto equivalente para {blue_product.id} con color '{color}'."))
                    total_errors += 1
                    continue

                try:
                    equiv_compatible_modules, created = compatibleModules.objects.get_or_create(product=equivalent_product)

                    equiv_compatible_modules.modules.set(blue_compatible_modules)
                    equiv_compatible_modules.save()

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Creado compatibleModules para {equivalent_product.id} con color '{color}'."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Actualizado compatibleModules para {equivalent_product.id} con color '{color}'."))

                    total_assigned += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al asignar módulos a {equivalent_product.id}: {e}"))
                    total_errors += 1
                    continue

        self.stdout.write(self.style.SUCCESS(f"Asignación completada: {total_assigned} asignados, {total_skipped} omitidos, {total_errors} errores."))
