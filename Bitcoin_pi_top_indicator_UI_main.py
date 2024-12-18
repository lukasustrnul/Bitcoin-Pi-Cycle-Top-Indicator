# -*- coding: utf-8 -*-
"""
@Author: Lukáš Ustrnul
@github: https://github.com/lukasustrnul
@Linkedin: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Thu Feb 29 2024

Description:
"Golden Ratio Fibonacci Multiplier and Pi Cycle Top Indicator"

Based on article: "The Golden Ratio Multiplier" from Philip Swift (@PositiveCrypto) on Medium
link: https://positivecrypto.medium.com/the-golden-ratio-multiplier-c2567401e12a
"""

import streamlit as st
from load_update_price_df import load_check_update_overwriteCSV_sequence
from top_indicator_content_prep import df_with_users_guess, prepare_data_for_plot, additional_information
from BTC_plot_with_future_estimate import plot_BTC_chart

# set layout of the page and title
st.set_page_config(layout="wide", page_title="Bitcoin (BTC) Pi Cycle Top Indicator")

# set the position and width of the content
left_boarder, content_col, right_boarder = st.columns([1,12,1])

# initiate function to update CSV with historical prices and load the data
df = load_check_update_overwriteCSV_sequence(return_df = True)

with content_col:
    # header of the page
    st.header('Bitcoin Pi Cycle Top Indicator', divider = "violet")
    
    # add introduction and disclaimer to navigate first-time user to important information
    st.write(""" **Disclaimer: Nothing contained in this web should be considered as investment or trading advice.**  
             Idea of this indicator comes from ["The Golden Ratio Multiplier"](https://positivecrypto.medium.com/the-golden-ratio-multiplier-c2567401e12a) 
             article from [Philip Swift](https://positivecrypto.medium.com/).  
             Read at the bottom of the page how to use this interactive tool.""")

    
    # add title for the following table
    st.write("### Table: Estimated Future Change")
    # add description for the table
    st.write("""Add your estimate of Bitcoin (BTC) price development.  
             You can edit the current values and add rows with a positive or negative daily change.  
             Only rows with values in both columns will be used to calculate the future price estimate in the chart below.
             """)

    # show table with guessed values
    guess_df = df_with_users_guess()

    # prepare data for plot
    df_with_guess = prepare_data_for_plot(df, guess_df)
    
    # make a gap under table to make the UI look nicer
    st.write("")
    st.write("")
    # add heading for the plot
    st.write("""### Bitcoin (BTC) Pi Cycle Top Indicator Chart""")
    # plot the data
    plot_BTC_chart(df_with_guess, df.index[-1])
    
    # divide the additional information content
    st.write("***")    
    additional_information()


