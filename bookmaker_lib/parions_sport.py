from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from utils import data_management
import time
import datetime
import re


months = {
    "janvier": "01",
    "février": "02",
    "mars": "03",
    "avril": "04",
    "mai": "05",
    "juin": "06",
    "juillet": "07",
    "août": "08",
    "septembre": "09",
    "octobre": "10",
    "novembre": "11",
    "décembre": "12"
}


def get_data():
    options = FirefoxOptions()
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.add_argument("--headless")

    browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(5)

    browser.get("https://www.enligne.parionssport.fdj.fr/paris-football")

    cookie = browser.find_element(By.ID, "popin_tc_privacy_button_3")
    cookie.click()

    time.sleep(3)

    for n in range(10):
        try:
            button = browser.find_element(By.CLASS_NAME, "wpsel-internalLink1")
            button.click()
        except:
            browser.execute_script("window.scrollBy(0,10000)", "")

        time.sleep(3)

    text_file = open("data/pages/parions-sport.txt", "w", encoding="utf-8")
    text_file.write('%s' % browser.page_source)
    text_file.close()

    browser.close()


def parse_data(data):
    soup_parions_sport = data_management.read_file("parions-sport")

    events = soup_parions_sport.find_all(class_="wpsel-eventBloc")

    for event in events:
        h2_tag = event.find("h2")

        if "Les paris  en direct" not in h2_tag.text:

            if "aujourd'hui" in h2_tag.text:
                day = datetime.datetime.now().strftime('%d/%m')
            else:
                date_split = re.split(r" ", h2_tag.text)
                day = "{}/{}".format(date_split[2], months[date_split[3]])

            blocs = event.find_all(class_="wpsel-bloc")

            for bloc in blocs:

                odds = bloc.find_all(class_="outcomeButton-data")

                if len(odds) > 1:

                    teams = bloc.find(class_="wpsel-desc")
                    daytime = bloc.find(class_="wpsel-timerLabel")

                    team_a = re.sub(r" (.+) - .+", "\\1", teams.text)
                    team_b = re.sub(r".+ - (.+) (À.+)?", "\\1", teams.text)

                    date = "{} {}".format(
                        day,
                        re.sub(r"À.(\d{2})h(\d{2})", "\\1:\\2", daytime.text)
                    )

                    odd_1 = re.sub(r"(.+),(.+) ", "\\1.\\2", odds[0].text)
                    odd_x = re.sub(r"(.+),(.+) ", "\\1.\\2", odds[1].text)
                    odd_2 = re.sub(r"(.+),(.+) ", "\\1.\\2", odds[2].text)

                    # Add row data in the dataframe
                    data = data_management.add_row(data, "parions-sport", team_a.lower(), team_b.lower(), odd_1, odd_x, odd_2, date)

    return data
