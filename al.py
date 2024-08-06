import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

need_learn_cnt = 0

def start_video(chrome: webdriver.Chrome):
    iframe = WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((
            By.XPATH, '//iframe[@id="mainFrame"]'
        )))
    try:
        chrome.switch_to.frame(iframe)
        video_time = WebDriverWait(chrome, 100).until(
            EC.presence_of_element_located((
                By.XPATH, '//input[@id="videoTime"]'
            )))
        video_time_str = video_time.get_attribute('value')
        time_t = sum(x*int(t) for x, t in zip([60*60, 60, 1], video_time_str.split(':'))) + 5
        
        print(f'[Video] time : {video_time_str}, gap seconds: {time_t}')

        for i in range(time_t):
            time.sleep(1)
            print(f'[Video] learning {i}/{time_t}...', end='\r')
        print('\n[Video] learning complete!')
    except Exception as e:
        print(f'[Video] {e}')
    finally:
        chrome.switch_to.parent_frame()

def start_learning(chrome: webdriver.Chrome):
    # close helper window
    chrome.switch_to.window(chrome.window_handles[-1])
    iframe=WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((
            By.XPATH, '//iframe[@id="learnHelperIframe"]'
        )))
    print('[Learning] close helper...')
    try:
        chrome.switch_to.frame(iframe)
        chrome.find_element(By.XPATH, '//a[contains(@class, "shut-btn")]').click()
    except Exception as e:
        print(f'[Learning] {e}')
        return

    # select class video
    chrome.switch_to.window(chrome.window_handles[-1])
    # get the uncomplete video list
    iframe=WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((
            By.XPATH, '//iframe[@class="contentIframe"]'
        )))
    
    print('[Learning] start learning...')
    try:
        chrome.switch_to.frame(iframe)
        elems = chrome.find_elements(By.XPATH, '//div[@class="s_sectionwrap"]/div[@itemtype="video"]')
        for elem in elems:
            status = int(elem.get_attribute("completestate"))
            name = elem.get_attribute("title")
            print(f'[Learning] {name} is {"complete" if status == 1 else "uncomplete"}')
            if status == 1:
                continue
            
            elem.click()
            start_video(chrome=chrome)
    except Exception as e:
        print(f'[Learning] {e}')
        return

    chrome.close()
    chrome.switch_to.window(chrome.window_handles[-1])


def entry_learning_page(chrome: webdriver.Chrome, page_number:int=1):
    global need_learn_cnt
    if page_number > 22:
        return

    # Open the URL
    WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((
            By.XPATH, '//div[@class="page-container"]//ul[@class="el-pager"]'
        )))
    
    print('[Entry] entry_learning_page')
    chrome.find_element(By.XPATH, f'//div[@class="page-container"]//ul[@class="el-pager"]//li[text()="{page_number}"]').click()
    elems = chrome.find_elements(By.XPATH, '//div[@class="ia-c-all"]')
    for elem in elems:
        try:
            status = elem.find_element(By.XPATH, './div[@class="ia-c_status_2"]').text
            if status == '已达标':
                continue
            
            elem.click()
            time.sleep(5)
            start_learning(chrome=chrome)
            need_learn_cnt += 1
        except Exception as e:
            # print(f'[Entry] {e}')
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

        print(chrome.window_handles)
        entry_learning_page(chrome, 1)
    except Exception as e:
        print(e)
    finally:
        print('in finally, need learn: ', need_learn_cnt)
        time.sleep(5)
        chrome.quit()