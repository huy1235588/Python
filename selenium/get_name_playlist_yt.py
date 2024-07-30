from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup

import time

def show_hidden_video(driver):
    buttons = driver.find_elements(
        By.CLASS_NAME, "yt-spec-button-shape-next--icon-button")
    ActionChains(driver).click(buttons[1]).perform()
    hideden_video = driver.find_element(
        By.CLASS_NAME, "ytd-menu-navigation-item-renderer")
    ActionChains(driver).click(hideden_video).perform()
    time.sleep(1)


def scroll_to_end_page(driver):
    # Cuộn trang đến cuối trang để tải hết nội dung
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")

    while True:
        # Cuộn xuống cuối trang
        ActionChains(driver).send_keys(
            Keys.END).scroll_by_amount(0, -500).perform()

        # Chờ một chút để nội dung mới được tải
        time.sleep(2)
        # driver.implicitly_wait(2)

        # Lấy chiều cao trang mới
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight")

        print(new_height)

        # Kiểm tra xem đã đến cuối trang chưa
        if new_height == last_height:
            break

        last_height = new_height


def get_list_video(playlist_video):
    videos = []
    id = len(playlist_video)

    for video in playlist_video:
        # Lấy tên tiêu đề
        title = video.find("a",
                           {"id": "video-title"})

        # Check nếu title tồn tại, nếu có thì lấy href
        if title:
            # Lấy link video
            link_video = title.get("href").split("&list=")[0]
            title = title.get_text(strip=True)
        else:
            title = ""
            link_video = ""

        # Lấy tên kênh channel
        channel = video.find("a",
                             {"class": "yt-simple-endpoint style-scope yt-formatted-string"})

        # Check nếu channel tồn tại, nếu có thì lấy href
        if channel:
            link_channel = channel.get("href")
            channel = channel.get_text(strip=True)
        else:
            channel = ""
            link_channel = ""

        videos.append({"ID": id,
                       "Title video": title,
                       "Channel": channel,
                       "Link Video":  link_video,
                       "Link Channel": link_channel})
        id = id - 1

    return videos


# Hàm lấy tiêu đề video
def get_title_video(playlist_video, key):
    title = playlist_video.find("a",
                                {"id": "video-title"})
    if key == "Title Video":
        if title:
            # Lấy link video
            title = title.get_text(strip=True).replace('"', '\\"')
        else:
            title = ""
        return (f"\t\t\"{key}\": \"{title}\",\n")

    elif key == "Link Video":
        if title:
            # Lấy link video
            link_video = title.get("href").split("&list=")[0]
        else:
            link_video = ""
        return (f"\t\t\"{key}\": \"{link_video}\",\n")


# Hàm lấy kênh video
def get_channel_video(playlist_video, key):
    channel = playlist_video.find("a",
                                  {"class": "yt-simple-endpoint style-scope yt-formatted-string"})
    if key == "Channel":
        if channel:
            # Lấy link video
            channel = channel.get_text(strip=True)
        else:
            channel = ""
        return (f"\t\t\"{key}\": \"{channel}\",\n")

    elif key == "Link Channel":
        if channel:
            # Lấy link video
            link_channel = channel.get("href").split("&list=")[0]
        else:
            link_channel = ""
        return (f"\t\t\"{key}\": \"{link_channel}\"\n")


# Hàm lưu vào file json
def save_to_json_file(playlist_video):
    with open("selenium/json/yt_playlist.json", "w", encoding='utf-8') as file:
        file.write("[\n")
        id = len(playlist_video)
        for video in playlist_video:
            file.write("\t{\n" +
                "\t\t\"Id\": " + str(id) + ",\n"+
                get_title_video(video, "Title Video") +
                get_title_video(video, "Link Video") +
                get_channel_video(video, "Channel") +
                get_channel_video(video, "Link Channel")
            )
            if id != 1:
                file.write("\t},\n")
            else:
                file.write("\t}\n")
            id = id - 1
        file.write("\n]")


def main(url):
    options = webdriver.ChromeOptions()
    # options.add_argument(f"user-data-dir={chrome_profile_path}")

    options.add_argument(
        r"--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")

    options.add_argument(r'--profile-directory=Default')

    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Chờ một chút để trang web tải hoàn tất
    time.sleep(1)

    # Hiện video bị ẩn
    show_hidden_video(driver)

    # Cuộn đến cuối trang bằng JavaScript
    scroll_to_end_page(driver)

    # Đợi một chút để xem kết quả
    time.sleep(1)

    html_content = driver.page_source

    # Đóng trình duyệt
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    # with open("selenium/txt/youtube_playlist.html", encoding='utf-8') as file:
    #     soup = BeautifulSoup(file, 'html.parser')

    playlist_video = soup.find_all("ytd-playlist-video-renderer",
                                   {"class": "style-scope ytd-playlist-video-list-renderer",
                                    "style-type": ""})

    # videos = get_list_video(playlist_video)

    save_to_json_file(playlist_video)

    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())


url = "https://www.youtube.com/playlist?list=PLkpy2OpMMRQ6cap3fKbgveTqWLS_xXfDL"
main(url)
