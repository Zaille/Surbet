from bookmaker_lib import zebet, winamax, france_pari, unibet, betclic, parions_sport
from utils import surebet_finder
import pandas as pd


bookmakers = {
    "zebet": {"active": True, "lib": zebet},
    "winamax": {"active": True, "lib": winamax},
    "france-pari": {"active": False, "lib": france_pari},  # Get data by category
    "unibet": {"active": True, "lib": unibet},
    # "betclic": {"active": True, "lib": betclic},
    "parions-sport": {"active": True, "lib": parions_sport}
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


if __name__ == '__main__':
    data = pd.DataFrame()

    # get_data()

    data = parse_data(data)
    surebet = surebet_finder.find_surebet(data)

    data.to_csv('data/csv/odds.csv', index=False)
    surebet.to_csv('data/csv/surebet.csv', index=False)
