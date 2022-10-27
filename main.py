from bookmaker_lib import zebet, winamax, france_pari, unibet, betclic
import pandas as pd


bookmakers = {
    "zebet": {"active": True, "lib": zebet},
    "winamax": {"active": True, "lib": winamax},
    "france-pari": {"active": False, "lib": france_pari},  # Error 403
    "unibet": {"active": False, "lib": unibet},  # Error : Need JavaScript activated ( Test with Selenium )
    "betclic": {"active": True, "lib": betclic}
}


def get_data():
    for key in bookmakers:
        bookmaker = bookmakers[key]
        if bookmaker["active"]:
            print("Getting", key, "data...")

            bookmaker["lib"].get_data()


def parse_data(df):
    for key in bookmakers:
        bookmaker = bookmakers[key]
        if bookmaker["active"]:
            print("Parsing", key, "data...")

            df = bookmaker["lib"].parse_data(df)

    return df


def get_max_odd(array, name):
    bookmaker = None
    max_odd = 0

    for match in array:
        if float(match[name]) > max_odd:
            bookmaker = match['bookmaker']
            max_odd = float(match[name])

    return [bookmaker, max_odd]


def find_surebet(df):
    print("Looking For Surebets...")

    surebet_df = pd.DataFrame()

    for i, r1 in df.iterrows():
        array = [r1]
        for j, r2 in df.loc[i+1:].iterrows():
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

            surebet_df = pd.concat([surebet_df, pd.DataFrame([row])], ignore_index=True)

            # if ratio < 1:
    return surebet_df


if __name__ == '__main__':
    data = pd.DataFrame()

    # get_data()

    data = parse_data(data)
    surebet = find_surebet(data)

    data.to_csv('data/csv/odds.csv', index=False)
    surebet.to_csv('data/csv/surebet.csv', index=False)
