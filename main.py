import streamlit as st
import pandas as pd
from gsheetInterface import write_data, get_first_date, is_new_data

current_year_number = 7


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
    if get_first_date(current_year_number) == dataframe['Date Registered'].iloc[0]:  # gets first row, date registered column
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

