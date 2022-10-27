import pandas as pd
from lib import winamax, zebet, betclic


def parse_data():
    data = pd.DataFrame()

    data = winamax.get_data(data)
    data = zebet.get_data(data)
    data = betclic.get_data(data)

    return data


def get_max_odd(array, name):
    bookmaker = None
    max_odd = 0

    for match in array:
        if float(match[name]) > max_odd:
            bookmaker = match['bookmaker']
            max_odd = float(match[name])

    return [bookmaker, max_odd]


def find_surebet(data):
    print("Looking For Surebets...")

    surebet = pd.DataFrame()

    for i, r1 in data.iterrows():
        array = [r1]
        for j, r2 in data.loc[i+1:].iterrows():
            if r1["date"] == r2["date"] and r1["team_a"] == r2["team_a"] and r1["team_b"] == r2["team_b"]:  # TODO: Handle different name
                array.append(r2)

        if len(array) > 1:
            [bookmaker_odd_1, max_odd_1] = get_max_odd(array, 'odd_1')
            [bookmaker_odd_x, max_odd_x] = get_max_odd(array, 'odd_x')
            [bookmaker_odd_2, max_odd_2] = get_max_odd(array, 'odd_2')

            ratio = 1 / max_odd_1 + 1 / max_odd_x + 1 / max_odd_2

            row = {
                "team_a": array[0]['team_a'],
                "team_b": array[0]['team_b'],
                "bookmaker_odd_1": bookmaker_odd_1,
                "value_odd_1": max_odd_1,
                "bookmaker_odd_x": bookmaker_odd_x,
                "value_odd_x": max_odd_x,
                "bookmaker_odd_2": bookmaker_odd_2,
                "value_odd_2": max_odd_2,
                "ratio": ratio
            }

            surebet = pd.concat([surebet, pd.DataFrame([row])], ignore_index=True)

            # if ratio < 1:
    return surebet


if __name__ == '__main__':
    data = parse_data()
    surebet = find_surebet(data)

    data.to_csv('data/odds.csv', index=False)
    surebet.to_csv('data/surebet.csv', index=False)
