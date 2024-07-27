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

    # Đợi cho đến khi nội dung mới tải
    wait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'pmHCK')))

    webs = driver.find_elements(By.CLASS_NAME, 'pmHCK')

    list_size_of_folder = ""

    for index in range(len(webs)):
        folders = driver.find_elements(By.CLASS_NAME, 'pmHCK')
        # Nhấp vào folder
        ActionChains(driver).double_click(folders[index]).perform()

        # Đợi cho đến khi nội dung mới tải
        time.sleep(1)

        files = driver.find_elements(By.CLASS_NAME, "jApF8d")

        size_gb = 0

        for index, file in enumerate(files):
            if index % 2 != 0:
                size_unit = file.text.split(" ")[1]
                size = float(file.text.split(" ")[0].replace(",", '.'))
                if size_unit == "MB":
                    size /= 1000
                size_gb += size

        list_size_of_folder += str(size_gb) + "\n"

        time.sleep(1)

        driver.back()

        time.sleep(1)

    driver.quit()

    with open("selenium/test.txt", "w") as file:
            file.write(list_size_of_folder)


link_gg_drive = "https://drive.google.com/drive/u/0/folders/1i7WiX3_08xGXytlI8DlJhd7OpOvrP_b3"
get_size_folder(link_gg_drive)
