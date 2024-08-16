from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from main_app.config import urls_lavka, webdriver_name
from bs4 import BeautifulSoup
import asyncio
from main_app.models import Product, Shop, UnitOfMeasure
from main_app.conversions_functions import get_lavka_unit_id
from django.utils import timezone


def parse_by_address(city, street, number):
    a = Lavka()
    # asyncio.run(a.pars("Москва, Таллинская улица", "34"))
    asyncio.run(a.pars(', '.join([city, street]), number))
    a.sql_script(city, street, number)


class Parser:
    '''!
    Определяет базавый класс используемый для парсинга всех сайтов
    '''

    def __init__(self, shop_id):
        '''!
        Инициализирует класс Parser.
        @param user_id
        @param shop_id
        '''
        self.options = webdriver.ChromeOptions()
        self.product_list = []
        self.shop_obj = Shop.objects.get(pk=shop_id)

    def sql_script(self, city, street, number):
        '''! Сохраняет в базу данных
        '''

        self.product_list = [dict(t) for t in set(tuple(d.items()) for d in self.product_list)]

        print("-----START_SAVE_BD-----")

        now = timezone.now()

        for x in self.product_list:
            unit_obj = get_lavka_unit_id(x['unit'])
            _, created = Product.objects.get_or_create(unit=unit_obj,
                                                       shop=self.shop_obj, name=x["name"],
                                                       price=x["price"], amount=x["amount"],
                                                       link=x["link"], address_city=city,
                                                       address_street=street, address_number=number,
                                                       created=now)

        print("-----END-----")


class Lavka(Parser):
    '''!
    Определяет класс используемый для парсинга лавки.
    '''

    def __init__(self):
        '''!
        Инициализирует класс Lavka.
        @param user_id int
        '''
        super().__init__(1)
        self.url_main = "https://lavka.yandex.ru"
        self.options.add_argument("--start-maximized")
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)
        self.options.headless = True
        self.options.page_load_strategy = 'eager'
        self.driver = Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 100)
        self.urls = urls_lavka
        self.sl_tags = dict(product_block="p10zc8qs", product_name="l4t8cc8", product_link="p11oed5n",
                            discount_price="b1bvai5j", no_discount_price="c1jd7nwq", amount_and_unit="iks4ndv")

    async def get_data_product(self, product):
        '''!
        Выделяет из блока с информацией о продукте нужную и записывает в БД
        @param product BeautifulSoup
        '''
        if (product.find(class_=self.sl_tags["product_name"]) is not None) and (
                product.find(class_=self.sl_tags["product_link"]) is not None):
            name = product.find(class_=self.sl_tags["product_name"]).get_text().replace('­', '')
            # print(name)
            if product.find(class_=self.sl_tags["discount_price"]) is not None:
                price = int(
                    product.find(class_=self.sl_tags["discount_price"]).get_text().replace('₽', '').replace(' ',
                                                                                                            '').replace(
                        ' ', ''))
            else:
                price = int(
                    product.find(class_=self.sl_tags["no_discount_price"]).get_text().replace('₽', '').replace(' ',
                                                                                                               '').replace(
                        ' ', ''))
            link = self.url_main + product.find(class_=self.sl_tags["product_link"])['href']
            am_un = product.find(class_=self.sl_tags["amount_and_unit"]).get_text()
            amount = float(am_un[:am_un.find(' ')].replace(',', '.'))
            unit = am_un[am_un.find(' ') + 1:]
            self.product_list.append({"name": name, "price": price, "link": link, "amount": amount, "unit": unit})
        else:
            # print("pass")
            pass

    async def get_data_html(self, html):
        '''!
        Разбивает html код на блоки по продуктам, асинхронно запускает их обработку
        @param html string
        '''

        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all(class_=self.sl_tags["product_block"])
        tasks = []
        loop2 = asyncio.get_event_loop()
        for product in products:
            task = loop2.create_task(self.get_data_product(product))
            tasks.append(task)
        await asyncio.wait(tasks)

    async def pars(self, city_street, home):
        '''!
        Парсит список продуктов с ценами яндекс лавки по определенному адресу
        Производит запись в базу данных
        @param city_strit string
        @param home string
        '''
        print("pars_start")
        self.driver.get(self.url_main + "/10743/category/ovoshchi_griby_i_zelen")
        ukaz_adr = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/header/div[5]/button')))
        ukaz_adr.click()
        print("adr_start")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c12fmzph')))
        await asyncio.sleep(1)
        kr = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/button')))
        kr.click()
        adr_inp = self.driver.find_element(By.CLASS_NAME, 'i164506l')
        for lit in city_street:
            adr_inp.send_keys(lit)
            await asyncio.sleep(0.1)
        adr_inp.send_keys(' ')
        await asyncio.sleep(1)
        for lit in home:
            adr_inp.send_keys(lit)
            await asyncio.sleep(1)
        await asyncio.sleep(5)
        adr_inp.send_keys(Keys.DOWN)
        adr_inp.send_keys(Keys.ENTER)
        ok = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button')))
        ok.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 's17r5x1')))
        print("adr_finish")
        k = 6

        for j in range(0, k):
            tasks = []
            loop1 = asyncio.get_event_loop()

            i = j
            tabi = 1
            while i < len(self.urls):
                self.driver.execute_script(f"window.open('{self.urls[i]}', 'tab{tabi}');")
                i = i + k
                tabi = tabi + 1
            i = j
            tabi = 1
            while i < len(self.urls):
                self.driver.switch_to.window(f'tab{tabi}')
                html = self.driver.page_source
                task = loop1.create_task(self.get_data_html(html))
                tasks.append(task)
                i = i + k
                tabi = tabi + 1
            await asyncio.wait(tasks)

        self.driver.quit()

# a = Lavka()
# asyncio.run(a.pars("Москва, Таллинская улица","34"))
