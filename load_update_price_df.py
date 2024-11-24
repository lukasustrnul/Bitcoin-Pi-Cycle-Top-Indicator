# -*- coding: utf-8 -*-
"""
@Author: Lukáš Ustrnul
@github: https://github.com/lukasustrnul
@Linkedin: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Thu Feb 29 2024

Description:
    Set of functions which loads necessary data to dataframe, check if data are up-to-date and update them if necessary
"""
# import libraries
import pandas as pd
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import streamlit as st


def last_date_updated(df: pd.DataFrame) -> date:
    """
    finds and returns last date in the dataframe
    """
    last_date_updated = df.iloc[-1,0]
    return last_date_updated



# define functions
def yesterdays_date() -> date:
    """
    returns yesterday's date
    """
    # get today's date
    today = date.today()
    # calculate yesterday's date
    yesterday_datetime = today - timedelta(days=1)
    yesterday = pd.to_datetime(yesterday_datetime)
    return yesterday



def load_BTC_data() -> pd.DataFrame:
    """
    loads last saved version of csv file containing historical prices of bitcoin (BTC)
    In addition, casts Date column to datetime type
    
    Returns:
        dataframe with all historical prices of bitcoin
    """
    df = pd.read_csv("BTC-USD_price.csv")
    df["Date"]= pd.to_datetime(df["Date"])
    return df
    


def check_if_upto_date(df: pd.DataFrame) -> bool:
    """
    Function takes dataframe with dates and prices of an asset and check if the data are up to date.
    """
    # get the last date in the dataframe
    last_time_updated = last_date_updated(df)
    # get yesterday's date
    yesterday = yesterdays_date()
    # in an up-to-date Dataframe the last date should be yesterday's date because we are using Close price
    df_is_updated = last_time_updated == yesterday
    return df_is_updated


@st.cache_data(ttl=60*60*24)
def get_data_for_update_old() -> pd.DataFrame:
    """
    Scraps latest historical prices of bitcoin from yahoo finance using BeautifulSoup
    """ 
    # URL of a website containing historical Bitcoin prices
    url = "https://finance.yahoo.com/quote/BTC-USD/history"
    # Set a legitimate user-agent (more at https://stackoverflow.com/questions/68259148/getting-404-error-for-certain-stocks-and-pages-on-yahoo-finance-python)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }

    # Download the HTML content
    response = requests.get(url, headers = headers, timeout = 5)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the relevant table element (<tbody>)
    table = soup.find("tbody")

    # Extract data from table rows
    data = []
    # Loop through each table row (<tr>)
    for row in table.find_all("tr")[1:]:
        # Create an empty dictionary to store data for each row
        row_data_dict = {}
        row_data_list = []

        # Loop through each table cell (<td>)
        for cell in row.find_all("td"):
            # Extract the text from the cell, removing any leading/trailing whitespace and potential non-breaking space characters
            cell_text = cell.text.strip().replace(',', '')
            # Extract all cells to a list of values values in the row
            row_data_list.append(cell_text)
        
        # Use the list of values of the row to fill columns
        # check that the list has 7 items to avoid faulty data
        if len(row_data_list) == 7:
            row_data_dict["Date"] = pd.to_datetime(row_data_list[0])
            row_data_dict["Open"] = float(row_data_list[1])
            row_data_dict["High"] = float(row_data_list[2])
            row_data_dict["Low"] = float(row_data_list[3])
            row_data_dict["Close"] = float(row_data_list[4])
            row_data_dict["Adj Close"] = float(row_data_list[5])
            row_data_dict["Volume"] = float(row_data_list[6])
        else:
            row_data_dict["error"] = "This row had an unexpected number of values"

        # Append the extracted data for each row to the list
        data.append(row_data_dict)

    # Create pandas DataFrame
    df = pd.DataFrame(data)
    # omit last line as it is likely current date values which will be changing further during the day
    df = df.iloc[0:-1,:]
    # sort the dataframe by date from the oldest on top to the newest data at the bottom
    if "Date" in df.columns:
        df.sort_values(by="Date", inplace=True, ignore_index=True)
    else:
        # Handle the case where 'Date' is missing (e.g., print a message)
        st.write("An error occurred in update of price data.")
    return df
    
    
@st.cache_data(ttl=60*60*24)
def get_data_for_update() -> pd.DataFrame:
    """
    Fetches the latest historical prices of Bitcoin from Yahoo Finance API.
    """ 
    # API endpoint URL for historical data
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?range=1y&interval=1d"
    headers = { 'User-Agent': 'Mozilla/5.0' }

    # Fetch the data in JSON format
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()

    # Parse the data to get timestamps and price information
    timestamps = data['chart']['result'][0]['timestamp']
    prices = data['chart']['result'][0]['indicators']['quote'][0]

    # Create a DataFrame from the parsed data
    df = pd.DataFrame({
        'Date': pd.to_datetime(timestamps, unit='s'),
        'Open': prices['open'],
        'High': prices['high'],
        'Low': prices['low'],
        'Close': prices['close'],
        'Volume': prices['volume']
    })

    # Remove rows with any missing data (if present)
    df.dropna(inplace=True)
    # Sort the dataframe by date from the oldest to the newest data
    df.sort_values(by="Date", inplace=True, ignore_index=True)

    return df

def update_df(df, update_file):
    try:
        # get the last date in last version of BTC price history
        last_date_uptodate = last_date_updated(df)
        # find the index of the same date in the update_file
        index_of_last_date_uptodate_in_update = update_file.index[update_file["Date"] == last_date_uptodate].tolist()
        # add 1 to the index to get index from which the new data should be taken and added to full history
        index_to_start = index_of_last_date_uptodate_in_update[0]+1
        data_to_add = update_file.iloc[index_to_start: , :]
        df_new = pd.concat([df, data_to_add], ignore_index=True)
        return df_new
    except:
        return df



def overwrite_price_file_with_update(df: pd.DataFrame) -> None:
    # Write the updated DataFrame to the CSV file (append mode)
    df.to_csv("BTC-USD_price.csv", mode='w', index=False)






        
def load_check_update_overwriteCSV_sequence(return_df: bool = False):
    current_data = load_BTC_data()
    if check_if_upto_date(current_data) == False:
        update_file = get_data_for_update()
        fullprice_history_df = update_df(current_data, update_file)
        overwrite_price_file_with_update(fullprice_history_df)
        if return_df:
            return fullprice_history_df
    else:
        pass



if __name__ == '__main__':
    load_check_update_overwriteCSV_sequence()



