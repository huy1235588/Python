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
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'pmHCK')))

    webs = driver.find_elements(By.CLASS_NAME, 'pmHCK')

    list_size_of_folder = ""

    for index in range(len(webs)):
        # for index in range(1):

        # Tìm toàn bộ folder month
        folders_month = driver.find_elements(By.CLASS_NAME, 'pmHCK')

        # Nhấp vào folder month
        ActionChains(driver).double_click(folders_month[index]).perform()

        time.sleep(1)
        wait = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pmHCK')))

        # Tìm toàn bộ folder
        folders = driver.find_elements(By.CLASS_NAME, 'pmHCK')

        for index in range(len(folders)):
            # for index in range(1):
            # Đợi cho đến khi nội dung mới tải
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'pmHCK')))

            # Tìm toàn bộ folder
            folders = driver.find_elements(By.CLASS_NAME, 'pmHCK')

            # Lấy tên folder
            folders_name = folders[index].find_element(By.CLASS_NAME, 'KL4NAf')
            # Chuyển tên folder thành code
            folders_name = folders_name.text.split(" ")[0]

            max_index = range(len(folders))
            middle_index = max_index / 2

            # Nhấp vào folder
            if index == 0:
                ActionChains(driver).double_click(folders[0]).perform()
            elif index == middle_index:
                reverse_name = driver.find_element(By.CLASS_NAME, "ncj6Ve")
                reverse_index = max_index - middle_index
                ActionChains(driver).click(reverse_name).perform()
                for _ in range(reverse_index):
                    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
                ActionChains(driver).send_keys(Keys.ENTER).perform()
            else:
                for _ in range(index):
                    ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
                ActionChains(driver).send_keys(Keys.ENTER).perform()

            # Đợi cho đến khi nội dung mới tải
            WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'jApF8d')))

            # Tìm toàn bộ file trong folder, NHƯNG NÓ BAO GỒM CẢ NGÀY THÁNG
            files = driver.find_elements(By.CLASS_NAME, "jApF8d")

            size_gb = 0

            for file in (files):
                # Vì biến (file) chứa ngày tháng và kích thước file nên phải lọc ra
                # print(file.text)
                file = file.text
                if "MB" in file or "GB" in file:
                    # Lấy đơn vị MB, GB
                    size_unit = file.split(" ")

                    # Lấy giá trị size
                    size = file.split(" ")[0]
                    # Chuyển (size) 1.000 thành 1000 và 2,0 thành 2.0
                    size = size.replace(".", "").replace(",", '.')
                    # Chuyển (size) thành float
                    size = float(size)

                    # Chuyển MB sang GB
                    if size_unit == "MB":
                        size /= 1000
                    size_gb += size

            list_size_of_folder += f"{folders_name} " + \
                "\t" + f"{size_gb:.2f}" + "GB\n"

            time.sleep(2)

            # Lùi lại trang trước
            driver.back()

            # time.sleep(1)
            # Kết dòng for thứ 2

        list_size_of_folder += "\n"
        time.sleep(1)

        driver.back()

        # time.sleep(1)
        # Kết dòng for thứ 1

    driver.quit()

    with open("selenium/test.txt", "w") as file:
        file.write(list_size_of_folder)


link_gg_drive = "https://drive.google.com/drive/u/0/folders/1fDH7rpDw80rLK87ea9oV1gJfGr6t0RX3"
get_size_folder(link_gg_drive)
