# -*- coding: utf-8 -*-
"""
@Author: Lukáš Ustrnul
@github: https://github.com/lukasustrnul
@Linkedin: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Thu Feb 29 2024

"""

import pandas as pd
import numpy as np
        
        

def calc_simple_moving_average(df: pd.DataFrame, source_column: str, new_column: str, period_days: int) -> pd.DataFrame:
    """
    Calculates simple moving average (SMA) over the specific period of previous days
    
    Args:
        df (pd.DataFrame): The Dataframe containing columns with price of an asset
        source_column (str): name of the column containing the prices from which we will calculate SMA
        new_column (str): name of the column in which we will save SMA values
        period_days (int): number of rolling days from which to calculate SMA
    
    Returns:
        pd.DataFrame: Dataframe with all original data and new column with the SMA values
    """
    df[new_column] = df[source_column].rolling(window = period_days).mean()
    return df


def crossunder(df, line1, line2):
  """
  This function checks for crossovers between two SMA columns in a DataFrame.
  In addition the crossover is calsulated for 1.62 and 2.0 coefficient of the SMA with longer period.

  Args:
      df (pd.DataFrame): The DataFrame containing the columns to compare.
      line1 (str): The name of the first column, typically SMA values for shorter time period (e.g. 111 days)
      line2 (str): The name of the second column, typically SMA values for longer time period (e.g. 350 days)

  Returns:
      pd.Series: A Series indicating True for crossover points and False otherwise.
  """

  # Check if columns exist
  if line1 not in df.columns or line2 not in df.columns:
    raise ValueError("Columns not found in DataFrame")

  # Calculate crossover points using logical operators
  df['crossunder_2SMA_350'] = (df[line1] > 2*df[line2]) & (df[line1].shift(1) <= 2*df[line2].shift(1))
  df['crossunder_1.62SMA_350'] = (df[line1] > 1.618*df[line2]) & (df[line1].shift(1) <= 1.618*df[line2].shift(1))
  df['crossunder_SMA_350'] = (df[line1] > df[line2]) & (df[line1].shift(1) <= df[line2].shift(1))

  # Fill the first value with False (no crossover before the first data point)
  df.loc[0,'crossunder_2SMA_350'] = False
  df.loc[0,'crossunder_1.62SMA_350'] = False
  df.loc[0,'crossunder_SMA_350'] = False

  return df



def new_row_index(df: pd.DataFrame) -> int:
    """
    Returns value which should be the first index of newly added rows
    """
    first_index_of_guessed_data = df.index[-1]+1
    return first_index_of_guessed_data


def add_guess_to_df(df: pd.DataFrame, guess_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates new rows in df based on user guess from guess_df
    
    Returns:
        dataframe with additional rows for Date and Close column
    """
    # add rows and calculate Close price based on guess_df
    first_index_of_guessed_data = new_row_index(df)
    df_with_guess = df.copy()
    for index, row in guess_df.iterrows():
        if np.isnan(row['Period (days)']) or np.isnan(row['Daily Change (%)']):
            pass
        else:
            period_len = row['Period (days)']
            period_len = int(period_len)
            multiplier = 1+(row['Daily Change (%)']/100)
            for i in range(period_len):
                df_with_guess.loc[first_index_of_guessed_data+i,'Date'] = df_with_guess.loc[first_index_of_guessed_data+i-1,'Date']+pd.Timedelta(days = 1)
                df_with_guess.loc[first_index_of_guessed_data+i,'Close'] = df_with_guess.loc[first_index_of_guessed_data+i-1,'Close']*multiplier
            first_index_of_guessed_data += period_len
    return df_with_guess



if __name__ == '__main__':
    pass
