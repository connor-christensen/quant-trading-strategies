"""
Pairs Trading Strategy (Z-Score)
Computes the rolling price spread between two stocks and generates
long/short entry signals at ±2 standard deviations with exit 
signals when the spread returns to the mean.
"""

import yfinance as yf
import matplotlib.pyplot as plt

def stock_statistics(stocks):
    stocks["Spread"] = stocks["Close"]["TSLA"] - stocks["Close"]["AAPL"]
    stocks["MA20"] = stocks["Spread"].rolling(window=20).mean()
    stocks["Distribution"] = stocks["Spread"].rolling(window=20).std()
    stocks["Zscore"] = (stocks["Spread"] - stocks["MA20"]) / stocks["Distribution"]

def main():

    # Stock 1: TSLA, Stock 2: AAPL
    stocks = yf.download(["TSLA", "AAPL"], period="3y", progress=False)
    stock_statistics(stocks)

    # Count trading signals based on Z-score threshold crossings
    # Short when Z-score crosses above +2 (spread is unusually wide)
    short = ((stocks["Zscore"] > 2) & (stocks["Zscore"].shift(1) < 2)).sum()
    # Long when Z-score crosses below -2 (spread is unusually narrow)
    long = ((stocks["Zscore"] < -2) & (stocks["Zscore"].shift(1) > -2)).sum()
    # Exit when Z-score returns to within ±0.5 of the mean
    exit = ((stocks["Zscore"].between(-0.5, 0.5)) & ((stocks["Zscore"].shift(1) < -0.5) | (stocks["Zscore"].shift(1) > 0.5))).sum()

    print(f"Short Signals: {short}")
    print(f"Long Signals: {long}")
    print(f"Exits: {exit}")

    # Visualise Z-score with entry and exit thresholds
    stocks["Zscore"].plot()
    plt.title("Zscore Over 3 Years")
    plt.xlabel("Date")
    plt.ylabel("Z Score")
    plt.axhline(y=2.0, color = 'r', linestyle='--', label='Short Threshold')
    plt.axhline(y=-2.0, color = 'r', linestyle='--', label='Long Threshold')
    plt.axhline(y=0.5, color = 'r', linestyle='--', label='Exit Max')
    plt.axhline(y=-0.5, color = 'r', linestyle='--', label='Exit Min')
    plt.show()

main()