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

def gen_img(names,texts):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.headless = True
    driver = Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 600)
    driver.get("https://fusionbrain.ai/diffusion")
    cookie_yes = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div[4]/button')))
    cookie_yes.click()
    time.sleep(1)
    yes = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div[2]/div/div[2]')))
    yes.click()
    time.sleep(1)
    style = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[4]/div')))
    style.click()
    time.sleep(1)
    stud_photo = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[3]/div/div/div[2]/div[19]')))
    stud_photo.click()
    time.sleep(1)
    for i in range(0,len(names)):
        name=names[i]
        text=texts[i]
        final_text=f"Блюдо под названием: {name} \n Рецепт: \n  {text}"
        text_area = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[6]/div/textarea')))
        text_area.clear()
        text_area.send_keys(final_text)
        time.sleep(1)
        create = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[6]/button')))
        create.click()
        time.sleep(1)
        download1 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[3]/button[4]')))
        download1.click()
        time.sleep(1)
        download2 = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div[6]/div/button[1]')))
        download2.click()
        time.sleep(1)
    time.sleep(10)
nm="Шоколадные пирожные"
tx='''
1 - Разогрейте духовку до 180 градусов. Смажьте маслом противень размером 20 на 30 см и застелите бумагой для выпечки.

2 - В кастрюле растопите сливочное масло. Снимите с огня и добавьте какао, сахар и яйца.

3 - Просейте муку, разрыхлитель и щепотку соли и добавьте в масляную смесь. Хорошо перемешайте и добавьте мелко поломанный шоколад.

4 - Переложите тесто в форму и выпекайте 30 минут до готовности.

5 - Оставьте в форме на 10 минут, затем переложите на блюдо и охладите. Порежьте на кусочки.
'''
gen_img([nm,nm],[tx,tx])