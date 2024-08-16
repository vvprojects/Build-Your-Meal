import time
from bs4 import BeautifulSoup
import requests
import asyncio
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from main_app.functions_backend import string_to_minutes, number_and_measure
from main_app.models import Country, Type, SubType, Dish, CookingStage, Category,\
                            DishCategory, UnitOfMeasure, Conversion


url = "https://eda.ru"


async def get_recept(link):
    await asyncio.sleep(2)

    # информация о блюде - Dish, Country, Type, SubType
    page = requests.get(url+link)
    soup = BeautifulSoup(page.text, "html.parser")
    name = soup.find(class_="emotion-gl52ge").text
    if await sync_to_async(Dish.objects.filter(name=name).exists)():
        return 1
    block_tags = soup.find(class_="emotion-19rdt1j")
    tags = block_tags.find_all(class_="emotion-1h6i17m")
    country = None
    for tag in tags:
        if "кухня" in tag.text:
            country = tag.text
    if country is None:
        return 1
    dish_type = tags[1].text
    subtype = tags[-1].text
    bloc_pic = soup.find(class_="emotion-182ex74")
    pic_link = bloc_pic.find("img")['src']
    porc = soup.find(itemprop="recipeYield").text
    cooking_time = string_to_minutes(soup.find(class_="emotion-my9yfq").text)
    cal = soup.find(itemprop="calories").text
    bel = soup.find(itemprop="proteinContent").text
    fat = soup.find(itemprop="fatContent").text
    ug = soup.find(itemprop="carbohydrateContent").text

    # этапы готовки - CookingStage
    step_list = []
    step_blocks = soup.find_all(itemprop="recipeInstructions")
    for step_block in step_blocks:
        step_num = step_block.find(class_="emotion-1hreea5").text
        step_text = step_block.find(itemprop="text").text
        if step_block.find("img") is not None:
            step_img = step_block.find("img")["src"]
        else:
            step_img = None
        step_list.append({'step_text': step_text, 'step_num': step_num, 'step_img': step_img})

    # ингридиенты - DishCategory, UnitOfMeasure, Conversion
    ing_list = []
    ings = soup.find_all(class_="emotion-7yevpr")
    for ing in ings:
        ing_name = ing.find(itemprop="recipeIngredient").text
        if not await sync_to_async(Category.objects.filter(name=ing_name).exists)():
            return 1
        ing_kol_vo, ing_unit = number_and_measure(ing.find(class_="emotion-bsdd3p").text)

        ing_list.append({'ing_name': ing_name, 'ing_kol_vo': ing_kol_vo, 'ing_unit': ing_unit})

    # записываем данные в БД
    country_obj, _ = await sync_to_async(Country.objects.get_or_create)(name=country)
    type_obj, _ = await sync_to_async(Type.objects.get_or_create)(name=dish_type)
    subtype_obj, _ = await sync_to_async(SubType.objects.get_or_create)(type=type_obj, name=subtype)
    dish_obj = Dish(country=country_obj, subtype=subtype_obj, name=name, pers_num=int(porc),
                    cooking_time_minutes=cooking_time, image=pic_link, calories=int(cal),
                    proteins=int(bel), carbohydrates=int(ug), fats=int(fat))
    await sync_to_async(dish_obj.save)()
    for i in ing_list:
        cat = await sync_to_async(Category.objects.exclude(supreme_category__isnull=True).get)(name=i['ing_name'])
        unit, _ = await sync_to_async(UnitOfMeasure.objects.get_or_create)(name=i['ing_unit'])
        dish_cat_obj = DishCategory(dish=dish_obj, category=cat, unit=unit, amount=i['ing_kol_vo'])
        await sync_to_async(dish_cat_obj.save)()
        conv, _ = await sync_to_async(Conversion.objects.get_or_create)(category=cat, from_unit=unit)
    for i in step_list:
        step_obj = CookingStage(dish=dish_obj, description=i['step_text'], order=i['step_num'], image=i['step_img'])
        await sync_to_async(step_obj.save)()

    return 0


async def pars_page(i):
    page = requests.get(url+f"/recepty?page={i}")
    soup = BeautifulSoup(page.text, "html.parser")
    bloks = soup.find_all(class_="emotion-1eugp2w")
    loop1 = asyncio.get_event_loop()
    for blok in bloks:
        task = loop1.create_task(get_recept(blok.find(class_="emotion-18hxz5k")['href']))
        await asyncio.wait([task])


class Command(BaseCommand):
    help = 'Parse Recipes'

    def handle(self, *args, **options):
        for i in range(1, 715):
            asyncio.run(pars_page(i))
            print(i)
            time.sleep(3)
