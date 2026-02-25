# -*- coding: utf-8 -*-
"""
Data provider for Streamlit app.
Prefers Yahoo Finance and falls back to local CSV if Yahoo is unavailable.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from load_update_price_df import fetch_yahoo_btc_data, load_BTC_data


@st.cache_data(show_spinner=False)
def _get_yahoo_data_cached_for_utc_day(cache_day_utc: str) -> pd.DataFrame:
    """
    Cache BTC data for the current UTC day.
    Cache invalidates at midnight UTC.
    """
    _ = cache_day_utc
    df = fetch_yahoo_btc_data()
    # Ignore the latest row as it can be an in-progress day candle.
    return df.iloc[:-1, :].copy()


def load_data_for_app() -> tuple[pd.DataFrame, str | None]:
    """
    Loads data for app usage.
    Primary source: Yahoo API (cached till UTC midnight).
    Fallback: local CSV in repository.
    """
    cache_day_utc = datetime.now(timezone.utc).date().isoformat()

    try:
        return _get_yahoo_data_cached_for_utc_day(cache_day_utc), None
    except Exception:
        fallback_df = load_BTC_data()
        warning = (
            "⚠️ Live Yahoo Finance data are temporarily unavailable. "
            "Loaded fallback data from the local CSV in this repository."
        )
        return fallback_df, warning
