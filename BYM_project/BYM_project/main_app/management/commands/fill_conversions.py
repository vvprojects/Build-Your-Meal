from django.core.management.base import BaseCommand
from main_app.models import Conversion, UnitOfMeasure, Category
import pandas as pd


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        df = pd.read_excel('final_convs.xlsx', dtype='str')

        for row in df.itertuples():
            try:
                cats = Category.objects.filter(name=row[1])
                for i in cats:
                    if i.supreme_category:
                        cat = i
                unit_from = UnitOfMeasure.objects.get(name=row[2])
                unit_to = UnitOfMeasure.objects.get(name=row[3])
                Conversion.objects.filter(category=cat, from_unit=unit_from, to_unit=unit_to).update(coefficient=row[4])
            except Exception as e:
                print(str(e))
                print(row[1], row[2], row[3], row[4])
