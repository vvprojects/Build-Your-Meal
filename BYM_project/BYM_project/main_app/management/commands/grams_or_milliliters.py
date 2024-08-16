from django.core.management.base import BaseCommand
from main_app.models import Conversion, UnitOfMeasure
import openai
import time


openai.api_key = ""


def model1(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": text}
        ]
    )
    return completion.choices[0].message.content


def model2(text):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return completion.choices[0].text


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        gram = UnitOfMeasure.objects.get(id=1)
        milliliter = UnitOfMeasure.objects.get(id=7)

        categories = []

        i = 0
        convs = Conversion.objects.all()

        for conv in convs:
            if conv.to_unit == gram or conv.to_unit == milliliter:
                continue

            # пропускаем уже пройденные категории
            if conv.category.name in categories:
                continue

            categories.append(conv.category.name)

            if i % 3 == 0:
                time.sleep(60)
            i += 1

            text = conv.category.name + ' это жидкость? Напиши только да или нет'
            print(i, '->', '(id =', conv.category.pk, ')', text)

            answer1 = model1(text).lower()
            print(answer1)

            if 'нет' in answer1:
                Conversion.objects.filter(category=conv.category).update(to_unit=gram)
            elif 'да' in answer1:
                Conversion.objects.filter(category=conv.category).update(to_unit=milliliter)
