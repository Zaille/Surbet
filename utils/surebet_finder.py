import re
import pandas as pd


def check_team_name(team_a, team_b):
    team_a_split = re.split(r" ", team_a)
    team_b_split = re.split(r" ", team_b)

    for team_a_elem in team_a_split:
        for team_b_elem in team_b_split:
            if len(team_a_elem) > 3 and len(team_b_elem) > 2 and team_a_elem == team_b_elem:
                return True

    return False


def get_max_odd(array, name):
    bookmaker = None
    max_odd = 0

    for match in array:
        if float(match[name]) > max_odd:
            bookmaker = match['bookmaker']
            max_odd = float(match[name])

    return [bookmaker, max_odd]


def get_loading(current_value, max_value, loading):
    if current_value > 0:
        res = 100 * current_value / max_value
        res_int = int(res)
        if res_int > loading:
            loading = res_int
            print("Loading: ", loading, "%")

    return loading


def already_saved(df, team_a, team_b, date):
    for index, row in df.iterrows():
        if date == row["date"] and check_team_name(team_a, row["team_a"]) and check_team_name(team_b, row["team_b"]):
            return True

    return False


def find_surebet(df):
    print("Looking For Surebets...")

    loading = 0

    surebet_df = pd.DataFrame()

    for i, r1 in df.iterrows():

        if not already_saved(surebet_df, r1["team_a"], r1["team_b"], r1["date"]):

            loading = get_loading(i, len(df), loading)

            array = [r1]

            for j, r2 in df.loc[i+1:].iterrows():
                if r1["date"] == r2["date"] and check_team_name(r1["team_a"], r2["team_a"]) and check_team_name(r1["team_b"], r2["team_b"]):  # TODO: Handle different name
                    array.append(r2)

            if len(array) > 1:
                [bookmaker_odd_1, max_odd_1] = get_max_odd(array, 'odd_1')
                [bookmaker_odd_x, max_odd_x] = get_max_odd(array, 'odd_x')
                [bookmaker_odd_2, max_odd_2] = get_max_odd(array, 'odd_2')

                ratio = 1 / max_odd_1 + 1 / max_odd_x + 1 / max_odd_2

                row = {
                    "date": array[0]['date'],
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

                surebet_df = pd.concat([surebet_df, pd.DataFrame([row])], ignore_index=True)

    return surebet_df
