import time
import json

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = wd.ChromeOptions
driver = wd.Chrome(options=options(), service=Service(ChromeDriverManager().install()))

def get_recipe():
    data = open('./kor_eng_foodtitle.json', 'r', encoding='utf-8').read()
    rom_kor_foodDict = json.loads(data)
    print(rom_kor_foodDict)

    food_list = list(rom_kor_foodDict.values())
    print(food_list)

    recipe_dict = {}

    driver.get('https://www.10000recipe.com/index.html')

    for idx in range(len(food_list)):
        keyword = food_list[idx]
        try:
            driver.find_element(By.CSS_SELECTOR, '#srhRecipeText').send_keys(keyword)
            driver.find_element(By.CSS_SELECTOR, '#frmTopRecipeSearch > div > span > button').click()
            for n in range(1, 30):
                driver.find_element(By.CSS_SELECTOR, '#contents_area_full > ul > ul > li:nth-child(' + str(n) +
                                    ') > div > a').click()
                recipe_title = driver.find_element(By.CSS_SELECTOR, '#contents_area > div.view2_summary.st3 > h3').text

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # 요리 순서 처리
                recipe_content = ''
                steps = soup.find_all('div', {'class': 'view_step_cont'})
                for s in steps:
                    recipe_content = recipe_content + s.find('div', {'class': 'media-body'}).text.replace('\n', '')

                recipe_imgpath = driver.find_element(By.CSS_SELECTOR, '#main_thumbs').get_attribute('src')
                print([recipe_title, recipe_content, recipe_imgpath])
                if recipe_content is None:
                    continue
                recipe_dict[recipe_title] = [recipe_title, recipe_content, recipe_imgpath]
                driver.back()
        except Exception:
            continue
    print(recipe_dict)