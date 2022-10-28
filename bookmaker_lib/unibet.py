from utils import data_management
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import re


def get_data():
    options = FirefoxOptions()
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.add_argument("--headless")

    browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(5)

    browser.get("https://www.unibet.fr/sport/football")

    for n in range(10):
        browser.execute_script("window.scrollBy(0,10000)", "")
        time.sleep(3)

    text_file = open("data/pages/unibet.txt", "w", encoding="utf-8")
    text_file.write('%s' % browser.page_source)
    text_file.close()

    browser.close()


def parse_data(data):
    soup_unibet = data_management.read_file("unibet")

    events = soup_unibet.find_all(class_="calendar-event")

    for event in events:

        teams_div = event.find(class_="cell-event")

        if teams_div:

            teams = teams_div.find("span")
            teams_split = re.split(r" - ", teams.string)

            team_a = teams_split[0]
            team_b = teams_split[1]

            datetime_string = event.find(class_="datetime")

            date = re.sub(r"(\d{2}/\d{2})/\d{4} (\d{1,2}:\d{2})", "\\1 \\2", datetime_string.text)
            if len(date) == 10:
                date = date[:6] + "0" + date[6:]

            odds_string = event.find_all(class_="odd-price")

            odd_1 = re.sub(r".+ (\d+(\.\d+)?)", "\\1", odds_string[0].text)
            odd_x = re.sub(r".+ (\d+(\.\d+)?)", "\\1", odds_string[1].text)
            odd_2 = re.sub(r".+ (\d+(\.\d+)?)", "\\1", odds_string[2].text)

            # Add row data in the dataframe
            data = data_management.add_row(data, "unibet", team_a.lower(), team_b.lower(), odd_1, odd_x, odd_2, date)

    return data
