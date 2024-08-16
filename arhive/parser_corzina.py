from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from config import urls_lavka, webdriver_name
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

options = webdriver.ChromeOptions()
url_main = "https://lavka.yandex.ru/"
options.add_argument("--start-maximized")
#options.headless = True
#options.page_load_strategy = 'eager'
driver = Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 600)

urls = urls_lavka[0]
products_ex=[{'product_link':'https://lavka.yandex.ru/213/good/57f9e9548cd74d1cb3033c6dcd002676000200010000','amount':2},
       {'product_link':'https://lavka.yandex.ru/213/good/4a46f152863c4f0ea4856565001e0919000300010000','amount':1}]
def do_order(products,user_id):
    driver.get("https://passport.yandex.ru/auth?origin=grocery-frontend-standalone&retpath=https%3A%2F%2Flavka.yandex.ru%2F213%2Fcart%3FpassportMetrikaPrevSource%3Dcart%26triggerRefreshPageInOtherTabs%3Dtrue")
    QR_b = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/div/button[4]')))
    QR_b.click()
    time.sleep(5)
    driver.save_screenshot(f'QR_{user_id}.png')
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/header/div[5]/button')))
    time.sleep(5)
    if 'c1vwcsci' in driver.page_source:
        driver.find_element(By.CLASS_NAME, 'c1vwcsci').click()
    #Проверяем корзину
    if driver.find_element(By.CLASS_NAME,"ttu50to").text=='Итого':
        #Чистим корзину
        clean_b = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div[1]/div/button')))
        clean_b.click()
        clean_b = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/button[2]')))
        clean_b.click()
    #Ввод адреса
    ukaz_adr = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/header/div[5]/button')))
    time.sleep(10**-1)

    ukaz_adr.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c12fmzph')))

    kr = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[1]/div/button')))
    kr.click()
    adr_inp = driver.find_element(By.CLASS_NAME, 'i164506l')
    for lit in "Москва, Таллинская улица":
        adr_inp.send_keys(lit)
        time.sleep(0.1)
    adr_inp.send_keys(' ')
    time.sleep(1)
    for lit in "34":
        adr_inp.send_keys(lit)
        time.sleep(1)
    time.sleep(5)
    adr_inp.send_keys(Keys.DOWN)
    adr_inp.send_keys(Keys.ENTER)
    ok = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button')))
    ok.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 's17r5x1')))
    time.sleep(5)
    #Ввод адреса конец


    for product in products:
        driver.get(product['product_link'])
        dobav = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-id"]/div[2]/div[2]/div/div[2]/button')))
        dobav.click()
        for plus_count in range(1,product['amount']):
            plus = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-id"]/div[2]/div[2]/div/div[2]/div/div/button[2]')))
            plus.click()
            time.sleep(0.1)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/header/div[7]/button')))

    while True:
        time.sleep(10)


do_order(products_ex,1)