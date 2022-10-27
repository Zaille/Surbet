from bs4 import BeautifulSoup
import pandas as pd


def read_file(filename):
    text_file = open("data/pages/" + filename + ".txt", "r")
    content = text_file.read()
    return BeautifulSoup(content, 'html.parser')  # Read content with Beautiful Soup


def addRow(data, bookmaker, team_a, team_b, odd_1, odd_x, odd_2, date):
    row = {
        "bookmaker": bookmaker,
        "team_a": team_a,
        "team_b": team_b,
        "odd_1": float(odd_1),
        "odd_x": float(odd_x),
        "odd_2": float(odd_2),
        "date": date
    }

    return pd.concat([data, pd.DataFrame([row])], ignore_index=True)