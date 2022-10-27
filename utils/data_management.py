from bs4 import BeautifulSoup
import pandas as pd


def read_file(filename):
    text_file = open("data/pages/" + filename + ".txt", "r", encoding="utf-8")
    content = text_file.read()
    return BeautifulSoup(content, 'html.parser')  # Read content with Beautiful Soup


def save_file(data, filename):
    text_file = open("data/pages/" + filename + ".txt", "w", encoding="utf-8")
    text_file.write('%s' % data)
    text_file.close()


def add_row(data, bookmaker, team_a, team_b, odd_1, odd_x, odd_2, date):
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