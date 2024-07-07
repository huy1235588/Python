from bs4 import BeautifulSoup
import requests
from datetime import datetime

link_calendar = "https://game8.co/games/Genshin-Impact/archives/297500"
link_datetime_vietnam = "https://www.timeanddate.com/worldclock/vietnam/ho-chi-minh"
link_datetime_algeria = "https://www.timeanddate.com/worldclock/algeria/algiers"

phase_2_check = "Phase 2"

# Get current time in vietnam


def getDateTime(link_url):
    reponse = requests.get(link_url)
    soup = BeautifulSoup(reponse.content, 'html.parser')

    current_datetime = soup.find(id="ctdat").get_text()

    # table = soup.find("table", {"class", "table--inner-borders-rows"})
    # tr = table.find_all("tr")
    # langues_zone = tr[4].find("th")

    return current_datetime

# check if phase = 2


def checkPhase(link_url):
    response = requests.get(link_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    element_phare = soup.find(id="hl_1")
    element_phare_text = element_phare.get_text()

    if phase_2_check in element_phare_text:
        table = element_phare.find_next_sibling("table")

        day_phase_2 = table.find("td").get_text().split()[1].replace(",", "")
        month_phase_2 = table.find("td").get_text().split()[0]
        year_phase_2 = table.find("td").get_text().split()[2]

        # datetime_phase_2 = datetime(
        #     year_phase_2,
        #     datetime.strptime(month_phase_2, '%B'),
        #     day_phase_2)

        current_datetime = getDateTime(link_datetime_vietnam)

        # current_date = datetime.now()
        # current_month = current_date.strftime("%B")
        # current_day = current_date.day  #

        # is_same_month = (month == current_month)
        # is_same_day = (int(day) == current_day)

        print(current_datetime)
    else:
        print(element_phare_text)


checkPhase(link_calendar)
