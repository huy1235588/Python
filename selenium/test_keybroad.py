from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

import time


def get_size_folder(url):
    # Đường dẫn đến hồ sơ Chrome của bạn
    chrome_profile_path = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Default"
    chromedriver_path = 'chromedriver/chromedriver.exe'

    options = webdriver.ChromeOptions()
    # options.add_argument(f"user-data-dir={chrome_profile_path}")

    options.add_argument(
        r"--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")

    options.add_argument(r'--profile-directory=Default')

    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    # Truy cập Google Drive
    driver.get(url)

    ActionChains(driver).key_down(Keys.ALT).send_keys(Keys.ARROW_RIGHT).key_up(Keys.ALT).perform()

    time.sleep(10)

    driver.quit()



link_gg_drive = "https://keytest.vn/"
get_size_folder(link_gg_drive)
