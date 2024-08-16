from django.core.management.base import BaseCommand
from main_app.functions_backend import number_and_measure
from main_app.models import DishCategory, UnitOfMeasure, Conversion


def parse_units():
    dish_category_objects = DishCategory.objects.all()
    for dish_category_object in dish_category_objects:
        string = dish_category_object.amount
        number, name = number_and_measure(string)

        unit, _ = UnitOfMeasure.objects.get_or_create(name=name)
        
        dish_category_object.unit = unit
        dish_category_object.amount = number
        dish_category_object.save()
        conversion_object = Conversion(category=dish_category_object.category, unit=unit, coefficient=1)
        conversion_object.save()
        

class Command(BaseCommand):
    help = 'Parse Units'

    def handle(self, *args, **options):
        parse_units()