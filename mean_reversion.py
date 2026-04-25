"""
Bollinger Band Mean Reversion Strategy
Uses a 20-day rolling Z-score to detect when price is far from its recent average,
and compares strategy returns against a buy-and-hold benchmark over 3 years.
"""

import yfinance as yf
import matplotlib.pyplot as plt

def main():

    stock = yf.download("MSFT", period="3y", progress=False)
    stock.columns = stock.columns.get_level_values(0)
    stock["MA20"] = stock["Close"].rolling(window=20).mean()
    stock["RollingStd"] = stock["Close"].rolling(window=20).std()
    stock["Return"] = stock["Close"].pct_change()

    # Z-score: how many standard deviations the current price is from the 20-day mean
    stock["Zscore"] = (stock["Close"] - stock["MA20"]) / stock["RollingStd"]

    # Bollinger Bands: upper and lower bounds at ±2 standard deviations from the mean
    bollinger_upper = stock["MA20"] + 2 * stock["RollingStd"]
    bollinger_lower = stock["MA20"] - 2 * stock["RollingStd"]

    # Stay in the market when Z-score is below 2 (exit when price is unusually high)
    stock["Signal"] = (stock["Zscore"] <=2).astype(int)
    stock["StrategyReturn"] = stock["Return"] * stock["Signal"]

    buy_hold_return = 1 + ((stock["Close"].iloc[-1] - stock["Close"].iloc[0]) / stock["Close"].iloc[0])
    total_strategy_return = ((1 + stock["StrategyReturn"]).cumprod()).iloc[-1]
    print(f"Buy and Hold Return: {buy_hold_return}")
    print(f"Strategy Return: {total_strategy_return}")

    # Plot 1: Price with Bollinger Bands
    # Plot 2: Z-score with entry/exit thresholds
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(stock["Close"], label="Close")
    ax1.plot(bollinger_upper, label="Upper Band", linestyle='--', color='r')
    ax1.plot(bollinger_lower, label="Lower Band", linestyle='--', color='g')
    ax1.set_title("Bollinger Bands")
    ax1.set_ylabel("Price (USD)")
    ax1.legend()

    ax2.plot(stock["Zscore"], label="Zscore")
    ax2.axhline(y=2.0, color='r', linestyle='--', label='Sell Threshold')
    ax2.axhline(y=-2.0, color='g', linestyle='--', label='Buy Threshold')
    ax2.set_title("Z Score")
    ax2.set_ylabel("Z Score")
    ax2.set_xlabel("Date")
    ax2.legend()

    plt.tight_layout()
    plt.show()







main()