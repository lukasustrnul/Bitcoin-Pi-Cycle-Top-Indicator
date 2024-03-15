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
import pandas as pd
from top_indic_calc import calc_simple_moving_average, crossunder, add_guess_to_df

################################################################################################################


def df_with_users_guess() -> pd.DataFrame:
    """
    Shows a table which can be changed by user to define user's guess of future change in bitcoin(BTC) price.
    Table contains one row of default values which can be edited
    """
    # initiate ataframe with first row of default values
    guess_df= pd.DataFrame({'Daily Change (%)':[0.1],'Period (days)':[100]})  
    # show the dataframe for editing
    guess_df = st.data_editor(guess_df, 
                              num_rows = "dynamic",
                              column_config={
                                  'Daily Change (%)': st.column_config.NumberColumn(help="insert positive or negative number for daily change in percents"),
                                  'Period (days)': st.column_config.NumberColumn(help="enter the number of days, we recommend using smaller values the larger is the 'Daily Change (%)' value")
                                  })
    return guess_df


def prepare_data_for_plot(df: pd.DataFrame, guess_df: pd.DataFrame) -> pd.DataFrame:
    """
    calculates table extended to the future based on original dataframe 
    (up to date daily historical prices of Bitcoin) and dataframe
    with users guess for the future
    
    Returns:
        dataframe extended to the future
    """
    # add rows and calculate Close price based on guess_df
    df_with_guess = add_guess_to_df(df, guess_df)

    # add columns with simple moving averages to the dataframe
    calc_simple_moving_average(df_with_guess, 'Close', 'SMA_111', 111)
    calc_simple_moving_average(df_with_guess, 'Close', 'SMA_350', 350)
    # calculate crossunder and add to the df
    df_with_guess = crossunder(df_with_guess, 'SMA_111','SMA_350')
    
    # return the final version of extended dataframe
    return df_with_guess



def additional_information():
    # motivation and function
    st.write("""#### Motivation and Function""")
    st.write("""Many people aiming to sell Bitcoin with maximum profit. However, bull market 
             and periods around new all-time-highs (ATH) are usually filled with extreme optimism
             which makes many to believe that the final ATH will come at much higher prices.
             The optimism is usually broken after significant correction of price and then the 
             opportunity to sell with the highest possible profit is long lost. 
             Using Fibonacci sequence and Pi cycle top indicator is one of the ways how to identify 
             top of the current cycle and sell on a reasonable moment.
             The complete explanation can be found in 
             ["The Golden Ratio Multiplier"](https://positivecrypto.medium.com/the-golden-ratio-multiplier-c2567401e12a) 
             article from [Philip Swift](https://positivecrypto.medium.com/).""")
    st.write("""While many platforms like TradingView allow you to add Fibonacci levels, 
             various SMAs (Single Moving Averages), and technical indicators, 
             it can be challenging for beginners to use these features effectively. 
             Additionally, these platforms often reserve advanced features like future price estimates for premium users.""")
    st.write("""**The Bitcoin Pi Cycle Top Indicator interactive tool empowers you to:**""")
    st.write("""- Effortlessly add future price estimates to Bitcoin chart.""")
    st.write("""- See how price estimates affect key indicators like SMAs.""")
    st.write("""- Visually identify potential turning points marked by the "big red cross" (indicating a new All-Time High).""")
    st.write("""- Test different scenarios to prepare your trading strategy.""")
    st.write("""- Make informed decisions by estimating the likelihood of the "Pi cycle top indicator" triggering a sell signal.""")
    
    # additional explanation of elements in the chart
    st.write("""#### Chart Explanation""")
    st.write("""Crosses in the chart indicates dates when SMA111 surpassed one of Fibonacci coefficients of SMA350 line. 
             Specifically, the color of cross is the same as color of SMA350 coefficient which was surpassed. 
             Therefore, small yellow cross for SMA350, medium beige cross for 1.62×SMA350 and big red cross for 2×SMA350.""")
    st.write("""In all previous cycles, a price very close to ATH was on the day when the SMA111 surpassed 2×SMA350 (big red cross).
             This is the main indicator of Pi Cycle Top Indicator""")
    
    # additional tips on how to use and interpret the data
    st.write("""#### Additional Tips""")
    st.write("""- Too large daily change may lead in just a few days to unrealistic values without trigerring
             the cross as the SMA for 111 days will not change so fast. Typically, average daily change around ATH is just few percent for couple of weeks.""")
    st.write("""- Add also periods of negative daily change if you trying to estimate price development in longer future. """)
    st.write("""- Since the beginning of Bitcoin, each next ATH was relatively lower in regards to Fibonacci coefficients of SMA350. 
             Around the last ATH in 2021 Bitcoin price reached roughly 3×SMA350; therefore we may consider an option
             that next ATH will be around 2×SMA350 levels and the undercross of SMA111 with 1.62×SMA350 could be indicating end of bull run.""")
    st.write("""- Chart can be switched to fullscreen, you can zoom in, move along x-axis using slider, 
             or zoom out to the whole chart by double-clicking inside the chart area""")
    
    # information about author and project
    st.write("""#### About Author and the Tool""")
    st.write("""Hi, my name is Lukas, I am a scientist and Bitcoin enthusiast.  
             To learn more about me or connect, please visit 
             [my LinkedIn profile](https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/).""")
    st.write("""If you are interested in the code, then check the project's 
             [repository at GitHub](https://github.com/lukasustrnul/Bitcoin-Pi-Cycle-Top-Indicator)""")
    st.write("""Bitcoin Pi Cycle Top Indicator Tool was developed using python and 
             [streamlit](https://streamlit.io/)""")
    st.write("""Overview of other useful indicators can be found at 
             [colintalkscrypto.com](https://colintalkscrypto.com/cbbi/)""")
 

  



if __name__ == '__main__':
    pass


