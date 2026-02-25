# -*- coding: utf-8 -*-
"""
@Author: Lukáš Ustrnul
@github: https://github.com/lukasustrnul
@Linkedin: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

Created on Thu Feb 29 2024

Description:
    Set of functions for loading and refreshing Bitcoin price data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests


YAHOO_BTC_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?range=50y&interval=1d"
CSV_FILE_PATH = Path("BTC-USD_price.csv")
CSV_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]


def load_BTC_data() -> pd.DataFrame:
    """
    Loads the repository CSV file containing historical BTC prices.
    """
    df = pd.read_csv(CSV_FILE_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def fetch_yahoo_btc_data(url: str = YAHOO_BTC_CHART_URL) -> pd.DataFrame:
    """
    Fetches full historical BTC daily OHLCV data from Yahoo Finance chart API.

    Returns:
        DataFrame with the same schema as BTC-USD_price.csv.
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.raise_for_status()
    payload = response.json()

    result = payload.get("chart", {}).get("result")
    if not result:
        raise ValueError("Yahoo response did not contain chart result data.")

    chart_data = result[0]
    timestamps = chart_data.get("timestamp")
    quote = chart_data.get("indicators", {}).get("quote", [{}])[0]
    adjclose = chart_data.get("indicators", {}).get("adjclose", [{}])[0]

    if not timestamps:
        raise ValueError("Yahoo response did not contain timestamps.")

    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(timestamps, unit="s", utc=True).tz_localize(None),
            "Open": quote.get("open"),
            "High": quote.get("high"),
            "Low": quote.get("low"),
            "Close": quote.get("close"),
            "Adj Close": adjclose.get("adjclose"),
            "Volume": quote.get("volume"),
        }
    )

    df = df.dropna(subset=["Close"]).copy()
    df = df[CSV_COLUMNS]
    df.sort_values(by="Date", inplace=True, ignore_index=True)
    return df


def write_price_csv(df: pd.DataFrame, output_path: Path = CSV_FILE_PATH) -> None:
    """
    Writes BTC price DataFrame to CSV using canonical column order.
    """
    clean_df = df.copy()
    clean_df["Date"] = pd.to_datetime(clean_df["Date"]).dt.strftime("%Y-%m-%d")
    clean_df.to_csv(output_path, index=False)


def generate_csv_from_yahoo(output_path: Path = CSV_FILE_PATH) -> pd.DataFrame:
    """
    Pipeline step that fetches Yahoo BTC data and writes CSV in project format.
    """
    df = fetch_yahoo_btc_data()
    write_price_csv(df, output_path=output_path)
    return df


if __name__ == "__main__":
    generate_csv_from_yahoo()
