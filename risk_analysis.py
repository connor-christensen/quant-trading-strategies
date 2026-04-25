"""
Risk Analysis Tool
Computes annualised return, annualised volatility, sharpe ratio, and maximum drawdown
for multiple stocks. Ranks them by risk-adjusted performance.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def stock_statistics(stock):
    """Compute and print risk metrics for a given stock."""
    # Annualise daily figures using 252 trading days per year
    annual_return = stock["Return"].mean() * 252
    annual_volatility = stock["Return"].std() * np.sqrt(252)
    sharpe = annual_return / annual_volatility

    # Drawdown: how far the price has fallen from its highest point so far
    stock["Drawdown"] = (stock["Close"] - stock["Peak"]) / stock["Peak"]
    max_drawdown = stock["Drawdown"].min()
    print(f"Annualised Return: {annual_return}")
    print(f"Annualised Volatility: {annual_volatility}")
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Max Drawdown: {max_drawdown}")
    return sharpe

def main():

    # Download 3 years of data and compute daily returns and running peak price
    tsla = yf.download("TSLA", period="3y", progress=False)
    tsla.columns = tsla.columns.get_level_values(0)
    tsla["Return"] = tsla["Close"].pct_change()
    tsla["Peak"] = tsla["Close"].cummax()
    nvda = yf.download("NVDA", period="3y", progress=False)
    nvda.columns = nvda.columns.get_level_values(0)
    nvda["Return"] = nvda["Close"].pct_change()
    nvda["Peak"] = nvda["Close"].cummax()
    msft = yf.download("MSFT", period="3y", progress=False)
    msft.columns = msft.columns.get_level_values(0)
    msft["Return"] = msft["Close"].pct_change()
    msft["Peak"] = msft["Close"].cummax()

    print("--- TSLA ---")
    sharpe_tsla = stock_statistics(tsla)
    print("\n\n--- NVDA ---")
    sharpe_nvda = stock_statistics(nvda)
    print("\n\n--- MSFT ---")
    sharpe_msft = stock_statistics(msft)

    # Rank stocks by Sharpe ratio 
    sharpe_dictionary = [
        {"ticker": "TSLA", "sharpe": sharpe_tsla},
        {"ticker": "NVDA", "sharpe": sharpe_nvda},
        {"ticker": "MSFT", "sharpe": sharpe_msft}
    ]


    print("\n--- Sharpe Ranking ---")

    sharpe_dictionary.sort(key=lambda x: x["sharpe"], reverse=True)
    for sharpe in sharpe_dictionary:
        print(f"{sharpe['ticker']}: {sharpe['sharpe']:.2f}")

    # Plot drawdown curves, comparing downside risk over time
    plt.plot(tsla["Drawdown"], label = "TSLA")
    plt.plot(nvda["Drawdown"], label = "NVDA")
    plt.plot(msft["Drawdown"], label = "MSFT")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.show()

main()