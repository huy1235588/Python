from bs4 import BeautifulSoup
import requests
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from requests_html import HTMLSession
from requests_futures.sessions import FuturesSession

import time

# link URL calendar
link_calendar_game8 = "https://game8.co/games/Genshin-Impact/archives/297500"
link_calendar_ign = "https://www.ign.com/wikis/genshin-impact/Banner_Schedule:_Current_and_Next_Genshin_Banners"

# link URL datetime
link_datetime_vietnam = "https://www.timeanddate.com/worldclock/vietnam/ho-chi-minh"
link_datetime_algeria = "https://www.timeanddate.com/worldclock/timezone/utc"
link_zeitverschiebung = "https://www.zeitverschiebung.net/en/city/1581130"
link_time_is = "https://time.is/Ho_Chi_Minh_City"
link_vietnamonline = "https://www.vietnamonline.com/current-time.html"
link_world_time_api = "https://worldtimeapi.org"

# Check if current phase is 2
phase_2_check = "Phase 2"


# Get current time in vietnam
def getDateTime(link_url):
    response = requests.get(link_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    current_datetime_class = soup.find("div", {"class", "s86_hd"})
    current_datetime_class_tb = current_datetime_class.find("div", {
        "class", "tb"})
    current_datetime_class_tb_cell = current_datetime_class_tb.find_all("div", {
        "class", "tb-cell"})
    current_datetime = current_datetime_class_tb_cell[1].get_text()

    return current_datetime

# convert datetime for phase 2
def convert_phase_2_to_datetime(date_str):
    # Định dạng của chuỗi ngày tháng, vd: "June 25, 2024"
    date_format = "%B %d, %Y"
    # Chuyển đổi chuỗi thành đối tượng datetime
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj

# Convert datetime for current
def convert_current_to_datetime(date_str):
    # Định dạng của chuỗi ngày tháng, vd: "Monday 08 July 2024"
    date_format = "%A %d %B %Y"
    # Chuyển đổi chuỗi thành đối tượng datetime
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj

# Convert datetime for current but no weekday


def convert_current_to_datetime_no_weekday(date_str):
    # Định dạng của chuỗi ngày tháng, vd: "28 June 2024"
    date_format = "%d %B %Y"
    # Chuyển đổi chuỗi thành đối tượng datetime
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj

# Get datime
def get_current_datetime():
    current_datetime_text = getDateTime(link_vietnamonline)
    current_datetime = convert_current_to_datetime(current_datetime_text)
    return current_datetime

# Compare two datetime
def compare_dates(date_before, date_after):
    elapsed_days = (date_after - date_before).days
    print(elapsed_days)

# check if phase = 2
def checkPhase(link_url):
    if ("game8" in link_url):
        response = requests.get(link_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        game8_phare = soup.find(id="hl_1")
        game8_phare_text = game8_phare.get_text()
        if phase_2_check in game8_phare_text:
            # Time phase 2
            table = game8_phare.find_next_sibling("table")
            phase_2_datetime_text = table.find(
                "td").get_text().split(" - ")[0].strip()
            phase_2_datetime = convert_phase_2_to_datetime(
                phase_2_datetime_text)
            # Time current
            current_datetime = get_current_datetime()

            # Compare phase 2 time And current time
            compare_dates(phase_2_datetime, current_datetime)


checkPhase(link_calendar_game8)
