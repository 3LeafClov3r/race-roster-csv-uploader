import streamlit as st
import pandas as pd
from gsheetInterface import *
from datetime import datetime, date


current_year_number = date.today().year


uploaded = False
uploaded_file = st.file_uploader("Upload csv here",type=".csv", accept_multiple_files=False)

data = None

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, dtype=str, usecols=['Participant ID', 'Date Registered', 'Bib Numbers', 'Last Name', 'First Name', 'Sex', 'Date of Birth', 'Email', 'City', 'State', 'Address', 'ZIP/Postal Code', 'Country', 'Sub-event', 'Age', 'Confirmation No.'])
    dataframe = pd.DataFrame(data).fillna("")
    st.write(dataframe)
    uploaded = True

submit = st.button("submit")

if submit and uploaded:
    stringg = dataframe['Date Registered'].iloc[0]
    stringg = stringg[:len(stringg)-4]
    year_of_csv = datetime.strptime(stringg, "%Y-%m-%d %H:%M:%S").year
    print(year_of_csv)
    if current_year_number == year_of_csv:
        match is_new_data(dataframe, current_year_number):
            case 0:
                st.write("Data already up to date")

            case 1:
                write_data(dataframe, current_year_number)
                st.write("New data uploaded")
            case 2:
                st.write("Too many values have been removed from the spreadsheet, try to upload a more recent sheet")
    else:
        st.write("Uploaded data is invalid, please check the year of data you are uploading for is the current year")

