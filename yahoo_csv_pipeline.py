"""
Pipeline utility for regenerating BTC-USD_price.csv from Yahoo Finance data.
"""

from pathlib import Path

from load_update_price_df import generate_csv_from_yahoo


if __name__ == "__main__":
    output_file = Path("BTC-USD_price.csv")
    generate_csv_from_yahoo(output_path=output_file)
    print(f"CSV refreshed from Yahoo Finance: {output_file}")
