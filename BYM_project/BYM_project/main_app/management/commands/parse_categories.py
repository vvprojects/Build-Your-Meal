import time
from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand
from main_app.models import Category


url = "https://eda.ru"


def pars_prod3(cat_obj_supreme2, link_cat2):
    time.sleep(2)
    page = requests.get(link_cat2)
    soup = BeautifulSoup(page.text, "html.parser")
    if soup.find(class_="emotion-1cyq6dp") is not None:
        blocks_cat3 = soup.find_all(class_="emotion-1cyq6dp")
        for block_cat3 in blocks_cat3:
            name_cat3 = block_cat3.text
            if name_cat3 != cat_obj_supreme2.name:
                cat_obj3 = Category(name=name_cat3, supreme_category=cat_obj_supreme2)
                cat_obj3.save()


def pars_prod2(cat_obj_supreme1, link_cat1):
    i = 1
    while True:
        time.sleep(3)
        page = requests.get(link_cat1 + f"?page={i}")
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.find(class_="emotion-17kxgoe") is None:
            break
        blocks_cat2 = soup.find_all(class_="emotion-17kxgoe")
        for block_cat2 in blocks_cat2:
            name_cat2 = block_cat2.find(class_="emotion-ogw7y8").text
            link_cat2 = url+block_cat2.find("a")['href']
            cat_obj2, created = Category.objects.get_or_create(name=name_cat2, supreme_category=cat_obj_supreme1)
            pars_prod3(cat_obj2, link_cat2)
        i = i + 1


def pars_prod1():
    page = requests.get("https://eda.ru/wiki/ingredienty")
    soup = BeautifulSoup(page.text, "html.parser")
    blocks_cat1 = soup.find_all(class_="emotion-19q74bd")
    for block_cat1 in blocks_cat1:
        name_cat1 = block_cat1.find(class_="emotion-13m5qdo").text
        link_cat1 = url+"/wiki/" + block_cat1.find("a")['href']
        cat_obj1 = Category(name=name_cat1, supreme_category=None)
        cat_obj1.save()
        pars_prod2(cat_obj1, link_cat1)
        time.sleep(1)
        print(name_cat1)


class Command(BaseCommand):
    help = 'Parse Categories'

    def handle(self, *args, **options):
        pars_prod1()
