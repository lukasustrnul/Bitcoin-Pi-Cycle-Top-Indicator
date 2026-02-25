# -*- coding: utf-8 -*-
"""
@Author: Lukáš Ustrnul
@github: https://github.com/lukasustrnul
@Linkedin: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Thu Feb 29 2024

"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def plot_BTC_chart(df: pd.DataFrame, last_index_of_real_data: int):
    """
    Plots a chart containing:
        price history, price future guess, SMA111, SMA350, 1.62*SMA35, 2*SMA350, markers for undercrosses
        
    Returns:
        plotly chart in streamlit
    """
    # make subsets of data to draw crosses where undercross
    subset_SMA_350 = df[df['crossunder_SMA_350']==True]
    subset_162SMA_350 = df[df['crossunder_1.62SMA_350']==True]
    subset_2SMA_350 = df[df['crossunder_2SMA_350']==True]
    
    # Create figure
    fig = go.Figure()
    SMA_width = 1
    # trace for historical Close price
    fig.add_trace(
        go.Scatter(x=list(df.loc[0:last_index_of_real_data+1,'Date']), 
                   y=list(df.loc[0:last_index_of_real_data+1,'Close']),
                   name = 'Daily Close Price - Historical',
                   marker={'color': '#30a347'},
                   line={'width':1.5},
                   opacity=1, 
                   ))
    # trace for guessed future Close price
    fig.add_trace(
        go.Scatter(x=list(df.loc[last_index_of_real_data+1:,'Date']), 
                   y=list(df.loc[last_index_of_real_data+1:,'Close']),
                   name = 'Daily Close Price - Estimate',
                   marker={'color': '#00ffff'},
                   line={'width':1.5},
                   opacity=1, 
                   ))
    
    # traces for SMA
    fig.add_trace(
        go.Scatter(x=list(df.Date), 
                   y=list(df.SMA_111),
                   name = '111 Days SMA',
                   marker={'color': '#d3444b'},
                   line={'width':SMA_width}
                   ))
    fig.add_trace(
        go.Scatter(x=list(df.Date), 
                   y=list(df.SMA_350),
                   name = '350 Days SMA',
                   marker={'color': '#d0a300'},
                   line={'width':SMA_width}
                   ))
    fig.add_trace(
        go.Scatter(x=list(df.Date), 
                   y=list(1.618*df.SMA_350),
                   name = '1.62 × 350 Days SMA',
                   marker={'color': '#edd9b3'},
                   line={'width':SMA_width}
                   ))
    fig.add_trace(
        go.Scatter(x=list(df.Date), 
                   y=list(2*df.SMA_350),
                   name = '2 × 350 Days SMA',
                   marker={'color': '#a37000'},
                   line={'width':SMA_width}
                   ))
    
    # traces for marker of undercross
    fig.add_trace(
        go.Scatter(x=[date for date in subset_SMA_350['Date']],
                   y=[1.1*i for i in subset_SMA_350['Close']],
                   mode="markers+text",
                   name="unedercross of SMA 350",
                   #text=["Text D" for i in range(len(subset_SMA_350))],
                   textposition="top center",
                   marker_symbol = "cross",
                   marker_size = 8,
                   marker_color = "#d0a300"
                   ))
    fig.add_trace(
        go.Scatter(x=[date for date in subset_162SMA_350['Date']],
                   y=[1.1*i for i in subset_162SMA_350['Close']],
                   mode="markers+text",
                   name="unedercross of 1.62* SMA 350",
                   #text=["Text D" for i in range(len(subset_162SMA_350))],
                   textposition="top center",
                   marker_symbol = "cross",
                   marker_size = 12,
                   marker_color = "#edd9b3"
                   ))
    fig.add_trace(
        go.Scatter(x=[date for date in subset_2SMA_350['Date']],
                   y=[1.1*i for i in subset_2SMA_350['Close']],
                   mode="markers+text",
                   name="unedercross of 2* SMA 350",
                   #text=["Text D" for i in range(len(subset_2SMA_350))],
                   textposition="top center",
                   marker_symbol = "cross",
                   marker_size = 16,
                   marker_color = "#d3444c"
                   ))
        
    # Set title
    fig.update_layout(
        #title_text="Bitcoin (BTC) Pi Cycle Top Indicator",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )
    
    # Add range slider and allow zooming along y axis
    fig.update_layout(
        xaxis=dict(
    
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        yaxis=dict(fixedrange=False,
        )
    )
    
    # Add log/linear scale switch buttons
    updatemenus = [
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"yaxis.type": "linear"}],
                    label="Linear Scale",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log"}],
                    label="Log Scale",
                    method="relayout"
                )
            ]),
            font=dict(color="green"),
            #showactive=True,
            x=-0.03,
            xanchor="right",
            y=1.1,
            yanchor="bottom"
            ),
    ]  
    
    # move the legend above the chart
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="center",
    x=0.5
    ))
    
    
    fig.update_layout(updatemenus=updatemenus)
    
    # Show the figure in the app
    BTC_plot = st.plotly_chart(fig, width='stretch')
    return BTC_plot



if __name__ == '__main__':
    pass