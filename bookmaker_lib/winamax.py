from utils import data_management
import requests
import re
import json
import datetime


def get_data():
    page = requests.get("https://www.winamax.fr/paris-sportifs/sports/1")

    data_management.save_file(page.content, "winamax")


def parse_data(data):
    soup_winamax = data_management.read_file("winamax")

    scripts = soup_winamax.find_all("script")  # Get <script> tag which contains data
    for script in scripts:
        if script.string and script.string.startswith('var PRELOADED_STATE'):
            inner_script = script.string  # Get content of the <script> tag
            json_string = inner_script[22:len(inner_script)-1]  # Get json which contains the data
            new_json_string = re.sub(r"\\(\\)?", '\\1', json_string)  # Remove unnecessary '\' in the JSON
            json_data = json.loads(new_json_string)  # Convert String to JSON

            matches = json_data["matches"]
            bets = json_data["bets"]
            outcomes = json_data["outcomes"]
            odds = json_data["odds"]

            for matchKey in matches:
                bet = bets[str(matches[matchKey]['mainBetId'])]
                if bet:
                    timestamp = matches[matchKey]['matchStart']  # Get match date and time
                    date = datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m %H:%M')  # Format date & time

                    outcomes_ids = bet["outcomes"]
                    if not re.match(r'\d - \d', outcomes[str(outcomes_ids[0])]['label']):  # Remove weird bets
                        team_a = outcomes[str(outcomes_ids[0])]['label']  # Get team A name
                        odd_1 = odds[str(outcomes_ids[0])]  # Get team A odd
                        if len(outcomes_ids) == 2:  # If it's a match with only 2 ways (e.g. tennis)
                            team_b = outcomes[str(outcomes_ids[1])]['label']
                            odd_x = 0
                            odd_2 = odds[str(outcomes_ids[1])]
                        else:  # If it's a match with more ways (e.g. foot)
                            team_b = outcomes[str(outcomes_ids[2])]['label']
                            odd_x = odds[str(outcomes_ids[1])]
                            odd_2 = odds[str(outcomes_ids[2])]

                        # Add row data in the dataframe
                        data = data_management.add_row(data, "winamax", team_a.lower(), team_b.lower(), odd_1, odd_x, odd_2, date)

    return data
