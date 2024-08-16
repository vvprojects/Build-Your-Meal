from django.core.management.base import BaseCommand
from main_app.models import Dish


def change_resolution():
    x = 500
    y = 300
    word = "c88x88"
    dish_objects = Dish.objects.all()
    for dish in dish_objects:
        index = str(dish.image).find(word)
        string = "c" + str(x) + "x" + str(y)
        new_image = str(dish.image)[:index] + string + str(dish.image)[index+len(word):]
        dish.image = new_image
        dish.save()


class Command(BaseCommand):
    help = 'Parse Categories'

    def handle(self, *args, **options):
        change_resolution()
