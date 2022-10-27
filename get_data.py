from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests


links = {
    "zebet": "https://www.zebet.fr/fr/sport/13-football",
    "winamax": "https://www.winamax.fr/paris-sportifs/sports/1",
    # "france-paris": "https://www.france-pari.fr/football"  # Error 403
    # "unibet": "https://www.unibet.fr/sport/football"  # Error : Need JavaScript activated ( Test with Selenium )
    "betclic": "https://www.betclic.fr/football-s1"  # Use Selenium to get all data
}


def save_data(name):
    print("Getting", name, "data...")

    # options = FirefoxOptions()
    # options.add_argument("--headless")

    # driver = webdriver.Firefox(options=options)
    # driver.get(links[name])

    # print(driver)

    page = requests.get(links[name])

    text_file = open("data/pages/" + name + ".txt", "w")
    text_file.write('%s' % page.content)
    text_file.close()


def get_data():
    for key in links:
        save_data(key)


if __name__ == '__main__':
    get_data()
