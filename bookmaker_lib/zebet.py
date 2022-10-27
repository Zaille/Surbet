from utils import data_management
import re
import requests


def get_data():
    page = requests.get("https://www.zebet.fr/fr/sport/13-football")

    data_management.save_file(page.content, "zebet")


def parse_data(data):
    soup_zebet = data_management.read_file("zebet")

    items = soup_zebet.find_all(class_="item")  # Bloc which contains all the containers with the bets

    for item in items:  # For each container

        blocs = item.find_all(class_="item-bloc")  # Get all matches

        for bloc in blocs:

            bet_event = bloc.find(class_="bet-event")

            if bet_event:
                teams_a_tag = bet_event.find('a')  # Tag which contains the teams name
                teams_text = teams_a_tag.string

                teams = re.split(r"\s/\s", teams_text)

                bet_time = bloc.find(class_="bet-time")
                date = re.sub(r'\\n\s{40}\\n\s{40}(.+)\s{40}(.+)\s{36}', '\\1 \\2', bet_time.string)  # Get date and time of the match

                odds = bloc.find_all(class_="pmq-cote")  # Get odds

                # TODO : Only work for football (not tennis)
                odd_1 = re.sub(r'\\n\s{8}(\d+),(\d+)\s{4}', '\\1.\\2', odds[0].string)
                odd_x = re.sub(r'\\n\s{8}(\d+),(\d+)\s{4}', '\\1.\\2', odds[1].string)
                odd_2 = re.sub(r'\\n\s{8}(\d+),(\d+)\s{4}', '\\1.\\2', odds[2].string)

                data = data_management.add_row(data, "zebet", teams[0].lower(), teams[1].lower(), odd_1, odd_x, odd_2, date)

    return data
