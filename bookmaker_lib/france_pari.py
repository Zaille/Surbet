from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_data():
    options = FirefoxOptions()
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.add_argument("--headless")

    browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(5)

    browser.get("https://www.france-pari.fr/football")

    text_file = open("data/pages/france-pari.txt", "w", encoding="utf-8")
    text_file.write('%s' % browser.page_source)
    text_file.close()

    browser.close()
