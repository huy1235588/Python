from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle

# Đường dẫn tới ChromeDriver
chromedriver_path = 'chromedriver/chromedriver.exe'

# Tạo thư mục lưu các tệp đã tải xuống
download_dir = "e:\Project\Python\selenium\downloads"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Cấu hình Chrome để tự động tải xuống tệp
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_dir,
         "directory_upgrade": True,
         "safebrowsing.enabled": True}
chrome_options.add_experimental_option("prefs", prefs)

# Khởi động trình duyệt Chrome với các tùy chọn đã cấu hình
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(chromedriver_path), options=chrome_options)

# Truy cập trang web
driver.get('https://sideload.betterrepack.com/download/AISHS2/Sideloader%20Modpack/hooh/')  # Thay bằng URL của trang web

# Đợi trang tải xong
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

# Tìm tất cả các thẻ <tr> trong thẻ <table>, ngoại trừ những thẻ có class "indexhead" và "even parent"
rows = table.find_elements(By.TAG_NAME, 'tr')

# Load trạng thái nếu có
state_file = 'e:\Project\Python\selenium\download_state.pkl'
if os.path.exists(state_file):
    with open(state_file, 'rb') as f:
        start_index = pickle.load(f)
else:
    start_index = 1


try:
    for i, row in enumerate(rows[start_index:], start=start_index):
        if "indexhead" not in row.get_attribute("class") and "even parent" not in row.get_attribute("class"):
            tds_tag = row.find_elements(By.CLASS_NAME, 'indexcolname')
            for td in tds_tag:
                link = td.find_element(By.TAG_NAME, 'a')
                href = link.get_attribute('href')
                if href and "download" in href:  # Điều kiện lọc thẻ <a> nếu cần
                    # print(link)
                    link.click()
                    time.sleep(3)  # Đợi tải xong, có thể điều chỉnh thời gian chờ tùy theo tình huống
except Exception as e:
    # Lưu trạng thái khi gặp lỗi
    with open(state_file, 'wb') as f:
        pickle.dump(i, f)
    print(f"An error occurred: {e}. Progress saved at row index {i}.")


# Đóng trình duyệt
driver.quit()
