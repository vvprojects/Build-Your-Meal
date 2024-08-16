# java -jar selenium-server.jar standalone
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from config import urls_lavka, webdriver_name
from bs4 import BeautifulSoup
import asyncio


class Parser:
    '''!
    Определяет базавый класс используемый для парсинга всех сайтов
    '''

    def __init__(self):
        '''!
        Инициализирует класс Parser.
        Забирает адрес вебдрайвера selenium из .env
        '''
        self.options = webdriver.ChromeOptions()

    async def sql_script(self, name, price, link, amount, unit_id):
        '''!
        Производит запись данных о продукте в базу данных.
        @param name string
        @param price int
        @param link string
        @param amount int
        @param unit_id int
        '''
        print(f"{name} {price} {link} {amount} {unit_id}")


class Lavka(Parser):
    '''!
    Определяет класс используемый для парсинга лавки.
    '''

    def __init__(self):
        '''!
        Инициализирует класс Lavka.
        Содержит ссылку на лавку.
        Задает опции для selenium.
        Задает время ожидания обновления сайта.
        Содержит список ссылок на  категории.
        '''
        super().__init__()
        self.url_main = "https://lavka.yandex.ru"
        self.options.add_argument("--start-maximized")
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.page_load_strategy = 'none'
        self.options.add_experimental_option("prefs", prefs)
        self.driver = Chrome(webdriver_name, options=self.options)
        self.wait = WebDriverWait(self.driver, 100)
        self.urls = urls_lavka

    async def get_data_product(self, product):
        '''!
        Выделяет из блока с информацией о продукте нужную и записывает в БД
        @param product BeautifulSoup
        '''
        if product.find(class_='lfklp1y') is not None:
            name = product.find(class_='lfklp1y').get_text().replace('­', '')
            if product.find(class_='b1g852u4') is not None:
                price = int(
                    product.find(class_='b1g852u4').get_text().replace('₽', '').replace(' ', '').replace(' ', ''))
            else:
                price = int(
                    product.find(class_='tmwo625').get_text().replace('₽', '').replace(' ', '').replace(' ', ''))
            link = self.url_main + product.find(class_='l1nk0t22')['href']
            am_un = product.find(class_='iks4ndv').get_text()
            amount = float(am_un[:am_un.find(' ')].replace(',', '.'))
            unit = am_un[am_un.find(' ') + 1:]
            await self.sql_script(name, price, link, amount, unit)

    async def get_data_html(self, html):
        '''!
        Разбивает html код на блоки по продуктам, асинхронно запускает их обработку
        @param html string
        '''
        soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(soup.text, 'html.parser')
        products = soup.find_all(class_='p10zc8qs')
        tasks = []
        loop2 = asyncio.get_event_loop()
        for product in products:
            task = loop2.create_task(self.get_data_product(product))
            tasks.append(task)
        await asyncio.wait(tasks)

    async def pars(self, j, city_street, home):
        '''!
        Парсит список продуктов с ценами яндекс лавки по определенному адресу
        Производит запись в базу данных
        @param j int номер старовой ссылки для нода
        @param city_strit string
        @param home string
        '''
        self.driver.get(self.url_main)
        await asyncio.sleep(5)
        await asyncio.sleep(j / 5)
        ukaz_adr = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/header/div[5]/button')))
        ukaz_adr.click()

        await asyncio.sleep(3)
        kr = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/button')
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
        ok = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button')
        await asyncio.sleep(2)
        ok.click()
        await asyncio.sleep(2)
        i = j
        k = 3
        while i < len(self.urls):
            url = self.urls[i]
            # self.driver.get(url)
            self.driver.get("view-source:" + url)
            await asyncio.sleep(2)
            html = self.driver.page_source
            loop1 = asyncio.get_event_loop()
            task = loop1.create_task(self.get_data_html(html))
            await asyncio.wait([task])
            i = i + k
        self.driver.quit()


async def main():
    '''!
    Функция для теста grid
    '''
    a0 = Lavka()
    a1 = Lavka()
    a2 = Lavka()
    # a3 = Lavka()
    # a4 = Lavka()
    loop = asyncio.get_event_loop()
    task0 = loop.create_task(a0.pars(0, "Москва, Таллинская улица", "34"))
    task1 = loop.create_task(a1.pars(1, "Москва, Таллинская улица", "34"))
    task2 = loop.create_task(a2.pars(2, "Москва, Таллинская улица", "34"))
    # task3 = loop.create_task(a3.pars(3,"Москва, Таллинская улица","34"))
    # task4 = loop.create_task(a4.pars(4,"Москва, Таллинская улица","34"))
    tasks = [task0, task1, task2]
    await asyncio.wait(tasks)


# Время работы 2 минуты

asyncio.run(main())
