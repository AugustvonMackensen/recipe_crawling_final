import time
import json

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium import webdriver as wd
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

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
        try:
            search = driver.find_element(By.CSS_SELECTOR, '#srhRecipeText')
            search.clear()

            keyword = food_list[idx]
            print(keyword)
            search.send_keys(keyword)
            click_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#frmTopRecipeSearch  \
                                                        > div > span > button')))
            driver.execute_script('arguments[0].click();', click_btn)
            for n in range(1, 40):
                time.sleep(5)
                li = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                      '#contents_area_full > ul > ul \
                                                                                      > li:nth-child(' + str(
                                                                                        n) + ') > div > a')))
                # Element is not clickable 방지 코드
                driver.execute_script('arguments[0].click();', li)
                recipe_title = driver.find_element(By.CSS_SELECTOR, '#contents_area > div.view2_summary.st3 > h3').text
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # 요리 순서 처리
                steps = soup.find_all('div', {'class': 'view_step_cont'})
                recipe_content = ''
                for s in steps:
                    recipe_content = recipe_content + s.find('div', {'class': 'media-body'}).text
                recipe_imgpath = driver.find_element(By.CSS_SELECTOR, '#main_thumbs').get_attribute('src')
                recipe_readcount = driver.find_element(By.CSS_SELECTOR, '#contents_area > div.view2_pic > div.view_cate.st2 > div > span').text
                print([recipe_title, recipe_content, recipe_imgpath, recipe_readcount])
                recipe_dict[recipe_title] = [recipe_title, recipe_content, recipe_imgpath, recipe_readcount]
                driver.back()
        except Exception as Msg:
            continue
    print(recipe_dict)
