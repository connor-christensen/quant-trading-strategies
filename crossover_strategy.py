"""
Moving Average Crossover Strategy
Backtests a 20/50-day moving average crossover strategy against a buy-and-hold benchmark
using 3 years of historical data from Yahoo Finance.
"""


import yfinance as yf
import matplotlib.pyplot as plt

def import_stock():
    """Download stock data and calculate returns, moving averages, and crossover signal."""
    ticker_input = input("Enter a stock ticker: ")
    stock = yf.download(ticker_input, period="3y", progress=False)
    stock["Returns"] = stock["Close"].pct_change()
    stock["MA20"] = stock["Close"].rolling(window=20).mean()
    stock["MA50"] = stock["Close"].rolling(window=50).mean()

    # Signal is True when short-term MA is above long-term MA
    signal = stock["MA20"] > stock["MA50"]
    return stock, signal

def returns(stock, signal):
    """Filter returns to only include days when the strategy is in the market."""
    in_market_returns = stock[signal]["Returns"]
    return in_market_returns


def return_statistics(stock, cumulative_3y_return, buy_hold_return):
    """Print strategy performance vs buy-and-hold, including trade count."""
    trades = trade_number(stock)
    print(f"Total Return Over 3 Years: {cumulative_3y_return.iloc[-1]:.4f}x")
    print(f"Buy and Hold Return: {buy_hold_return.iloc[-1]:.4f}x")
    print(f"Number of Trades: {trades}")

def trade_number(stock):
    """Count total trades by detecting MA crossover points (entries and exits)."""
    entry = (stock["MA20"] > stock["MA50"]) & (stock["MA20"].shift(1) < stock["MA50"].shift(1))
    exit = (stock["MA20"] < stock["MA50"]) & (stock["MA20"].shift(1) > stock["MA50"].shift(1))
    trades = entry.sum() + exit.sum()
    return trades
    

def main():

    stock, signal = import_stock()
    in_market_returns = returns(stock, signal)

    # Calculate cumulative returns for both strategy and benchmark
    cumulative_3y_return = (1+in_market_returns).cumprod()
    buy_hold_return = (1 + stock["Returns"]).cumprod()

    return_statistics(stock, cumulative_3y_return,buy_hold_return)

    # Plot strategy vs buy-and-hold cumulative returns
    plt.plot(cumulative_3y_return, label = "strategy")
    plt.plot(buy_hold_return, label = "hold")
    plt.title("Cumulative Return Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.show()



main()