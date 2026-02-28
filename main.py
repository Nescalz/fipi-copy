import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests as rc
import urllib3
import bs4 as soup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://oge.fipi.ru/",  
    "Connection": "keep-alive"
}
driver = webdriver.Chrome()
driver.get("https://oge.fipi.ru/bank/index.php?proj=DE0E276E497AB3784C3FC4CC20248DC0") #Ссылку суда

while True:
    iframe = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "questions_container"))
        )

        
    driver.switch_to.frame(iframe)

    block = driver.find_elements(By.XPATH, "//div[@class='qblock']")
    print(f"Найдено блоков: {len(block)}")
    for idx, b in enumerate(block, start=1):
        parse = soup.BeautifulSoup(b.get_attribute('outerHTML'), 'html.parser')

        imgs = b.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            img_url = img.get_attribute("src")
            print(img_url)

            response = rc.get(img_url, verify=False, headers=headers)
            print(response.status_code)

            if response.status_code == 200:
                print("Download")
                filename = os.path.basename(img_url)
                with open(f"images/{filename}", "wb") as f:
                    f.write(response.content)

        for img in parse.find_all("img"):
            old_src = img.get("src")   
            if old_src:
                filename = old_src.split("/")[-1]  
                new_src = f"images/{filename}"    

                img['src'] = new_src          
        with open("file.html", "a", encoding="utf-8") as file:
            content = file.write(f"{str(parse)}\n") 
    driver.switch_to.default_content()
    but = driver.find_element(By.XPATH, "//li[@class='active button']")
    but = driver.find_element(By.XPATH, f"//li[@class='button' and normalize-space(text())='{int(but.text) + 1}']").click()
