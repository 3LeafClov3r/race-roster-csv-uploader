from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import json


def get_gids_local_from_year(year_number:int):  # gets gids from local json instead of google api (keeping requests low)
    f = open('info.json')
    data = json.load(f)
    gid = ""
    for count, i in enumerate(data['name']):
        test = int(i)
        if test == year_number:
            gid = data['gid'][count]
            f.close()
            break
    return gid


def get_sheet_name_and_id():  # returns id then name in an array
    f = open('info.json')
    data = json.load(f)
    lst = [data['sheet_id'], data['sheet_name']]
    f.close()
    return lst


def setup():  # literally copied and pasted just allows for writing to spreadsheets
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    lst = get_sheet_name_and_id()
    sh = gc.open(lst[1])

    return sh


def get_gids():  # uses api to get gids
    sh = setup()
    return sh.worksheets()


def write_data(dataframe, year_number):  # actually writes to the sheet
    sh = setup()
    gid = get_gids_local_from_year(year_number)
    sh2 = sh.get_worksheet_by_id(gid)
    sh2.clear()
    sh2.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


def get_dataframe_by_year(year):  # returns dataframe from sheet
    lst = get_sheet_name_and_id()

    gid = get_gids_local_from_year(year)

    url = f"https://docs.google.com/spreadsheets/d/{lst[0]}/gviz/tq?tqx=out:csv&sheet={lst[1]}&gid={gid}"
    data = pd.read_csv(url, dtype=str).fillna("")
    df = pd.DataFrame(data)
    return df


def is_new_data(df, year_number):
    dataframe = get_dataframe_by_year(year_number)
    if dataframe.equals(df):
        return 0  # means same data
    else:
        if len(df.index) < len(dataframe.index) - 5:
            return 2  # means too much data will be removed
        return 1  # means upload new data


def get_first_date(year):  # checks if correct year by first registration date
    data = get_dataframe_by_year(year)
    return data['Date Registered'].iloc[0]

