from utils import data_management
import re
import datetime


def get_data(data):
    print("Parsing Betclic...")

    soup_betclic = data_management.read_file("betclic")

    group_events = soup_betclic.find_all(class_="groupEvents")

    for event in group_events:

        if event.find('h2').string != "Maintenant":

            sports_events = event.find_all("sports-events-event")

            for sport in sports_events:
                teams = sport.find_all(class_="scoreboard_contestantLabel")

                team_a = re.sub(r'\\n\s{12}\\n\s{12}(.+)\\n\s{8}', '\\1', teams[0].string)
                team_b = re.sub(r'\\n\s{12}(.+)\\n\s{8}', '\\1', teams[1].string)

                odds = sport.find_all(class_="oddValue")

                odd_1 = odds[0].string.replace(",", ".")
                odd_x = odds[1].string.replace(",", ".")
                odd_2 = odds[2].string.replace(",", ".")

                info_time = sport.find(class_="event_infoTime").string
                format_time = re.sub(r"\\n\s{12}(.+) (\d{2}:\d{2})\\n\s{8}", '\\1 \\2', info_time)
                time_split = re.split(r" ", format_time)

                if time_split[0] == "Aujourd\\'hui":
                    date = "{} {}".format(
                        datetime.datetime.now().strftime('%d/%m'),
                        time_split[1]
                    )
                elif time_split[0] == "Demain":
                    now = datetime.datetime.now().strftime('%d/%m')
                    date = "{} {}".format(
                        (datetime.datetime.strptime(now, '%d/%m') + datetime.timedelta(days=1)).strftime('%d/%m'),
                        time_split[1]
                    )
                elif time_split == "Après-demain":
                    now = datetime.datetime.now().strftime('%d/%m')
                    date = "{} {}".format(
                        (datetime.datetime.strptime(now, '%d/%m') + datetime.timedelta(days=2)).strftime('%d/%m'),
                        time_split[1]
                    )
                else:
                    date = "{} {}".format(
                        re.sub(r'(\d{2}/\d{2})/\d{4}', '\\1', time_split[0]),
                        time_split[1]
                    )

                # Add row data in the dataframe
                data = data_management.addRow(data, "betclic", team_a.lower(), team_b.lower(), odd_1, odd_x, odd_2, date)

    return data
