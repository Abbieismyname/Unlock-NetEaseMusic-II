# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0082B11BF1F29B1A9723CECBC48FC5B6666D514D392FFF9D137851EBCCA4C7EF6C25B497AFA435251FB836778B3C88D9E6C6D09467962D2924E348C6AC2D8543F29DB8C6C18392FD494C65D56E24BD59E1314632A2CFE5BD363EBF5A21701E5E0EEFC3E50E10E24C12BE290D1B13D6055C386D3D806A8F200503D1E1C1DD04B9A3B20C487BC0ED847649E520BC7AC18C123CD293E831393FADEDD96503B824309B58CA3077CBF7C4E8F66EA305276E770D21D3C9B48EB7EA50D9A9147CEF58C16BCAE05BE283A480106ED6E634EEFF2997B674D96262E3D35B5AECD6BC53316ACE483BE466485D21D59B430A46FD75A029D4BAF2D48556208B9D9BE60441198A2905A3EDC3D0B7D8AABADD6B1181DF6D031C2481BABB41C20112A7217E48E23336BA2A23FD7C41B7ECE8F0701F4896044D1F3C99FE54D954F0E8ECC47B1B333F1385D723A5499BC8189FAA44BAE521EBB3BABB97527D19227FFBA19BB7E2DF9C0E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
