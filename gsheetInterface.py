from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import json
import time
from class_init import *
from jsonHandling import *

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
        'secret_new_key.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    # lst = get_sheet_name_and_id()
    stuff = get_secure_info()
    info_gid = stuff[0]
    sheet_id = stuff[1]
    sheet_name = stuff[2]
    print(f"sheet_name:{sheet_name}")
    sh = gc.open(sheet_name)

    return sh


def get_gids():  # uses api to get gids
    sh = setup()
    return sh.worksheets()


def write_data(dataframe, year_number):  # actually writes to the sheet
    sh = setup()
    # gid = get_gids_local_from_year(year_number)
    info = Information()
    gid = info.get_gid_current_year()
    sh2 = sh.get_worksheet_by_id(gid)
    sh2.clear()
    sh2.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())





def is_new_data(df):
    info = Information()
    dataframe = info.get_current_df()
    if dataframe.equals(df):
        return 0  # means same data
    else:
        if len(df.index) < len(dataframe.index) - 5:
            return 2  # means too much data will be removed
        return 1  # means upload new data






def update_info_sheet(race_name: str, start_date:datetime, end_date:datetime, gid:int):
    sh = setup()
    info = Information()
    dataframe = info.dataframe
    dataframe.loc[len(dataframe.index)] = [race_name, start_date, end_date, str(gid)]
    sh2 = sh.get_worksheet_by_id(info.info_gid)
    sh2.clear()
    sh2.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())



def write_new_race(dataframe: pd.DataFrame, race_name: str, start_date:datetime, end_date:datetime) -> None:
    sh = setup()
    sh.add_worksheet(title=f"{race_name}")
    worksheets = sh.worksheets()
    time.sleep(6)
    for sheet in worksheets:
        if sheet.title == race_name:
            update_info_sheet(race_name, start_date, end_date, sheet.id)
            sh2 = sh.get_worksheet_by_id(sheet.id)
            sh2.clear()
            sh2.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
