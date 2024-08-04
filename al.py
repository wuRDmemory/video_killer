import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

need_learn_cnt = 0

def start_learning(chrome: webdriver.Chrome):
    pass

def entry_learning_page(chrome: webdriver.Chrome, page_number:int=1):
    global need_learn_cnt
    if page_number > 22:
        return

    # Open the URL
    WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((
            By.XPATH, '//div[@class="page-container"]//ul[@class="el-pager"]'
        )))
    
    print('entry_learning_page')

    chrome.find_element(By.XPATH, f'//div[@class="page-container"]//ul[@class="el-pager"]//li[text()="{page_number}"]').click()

    elems = chrome.find_elements(By.XPATH, '//div[@class="ia-c-all"]')
    for elem in elems:
        try:
            status = elem.find_element(By.XPATH, './div[@class="ia-c_status_2"]').text
            print('status: ', status)
            if status == '已达标':
                continue
            
            # elem.click()
            need_learn_cnt += 1
        except Exception as e:
            continue

    entry_learning_page(chrome=chrome, page_number=page_number+1)

if __name__ == '__main__':
    # url = 'https://studio.besteacher.com.cn/trainingGuidance/teacherHomePage'
    url = 'https://bj-sjs.besteacher.com.cn/basic/info/129678?t=1722776060346'
    user_path = r'C:\Users\wuch2\AppData\Local\Google\Chrome\User Data Copy'
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    option = webdriver.ChromeOptions()
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_argument('--disable-extensions')
    option.add_argument('--disable-gpu')
    option.add_argument('--user-data-dir=' + user_path)
    # option.add_argument('--remote-debugging-pipe')

    chrome = webdriver.Chrome(options=option)
    try:
        # Open the URL
        print('Open the URL', url)
        chrome.get(url=url)
        WebDriverWait(chrome, 100).until(
            EC.presence_of_element_located((
                By.XPATH, '//li[@class="el-menu-item"]'
            )))
        print('find the element')
        btn = chrome.find_element(By.XPATH, '//li[@class="el-menu-item"]')
        btn.click()

        entry_learning_page(chrome, 1)
    except Exception as e:
        print(e)
    finally:
        print('in finally, need learn: ', need_learn_cnt)
        time.sleep(5)
        chrome.quit()