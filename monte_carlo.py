"""
Monte Carlo Price Path Simulation
Generates 1,000 future price paths over 252 trading days using random returns
based on historical mean and standard deviation. Outputs expected price,
confidence bounds, and probability of positive return.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


def main():

    # Use 1 year of historical returns to estimate mean and standard deviation
    tsla = yf.download("TSLA", period="1y", progress=False)
    tsla.columns = tsla.columns.get_level_values(0)
    tsla["Return"] = tsla["Close"].pct_change()
    mean = tsla["Return"].mean()
    std = tsla["Return"].std()
    
    current_price = tsla["Close"].iloc[-1]
    paths = []

    # Simulate 1,000 price paths, each spanning 252 trading days (1 year)
    for sim in range(1000):
        path = [current_price]
        for day in range(252):
            # Each day's return is drawn randomly using the historical mean and std
            random_return = np.exp(mean + std * np.random.normal(0, 1))
            next_price = path[-1] * random_return
            path.append(next_price)
        paths.append(path)

    # Collect the final price from each simulation
    final_prices = []
    for idx in range (1000):
        final_prices.append(paths[idx][-1])
    expected_price = np.mean(final_prices)
    percentile_5th = np.percentile(final_prices, 5)
    percentile_95th = np.percentile(final_prices, 95)

    # Count how many simulations ended above the current price
    above = 0
    for p in final_prices:
        if p > current_price:
            above += 1
    probability = above / 1000

    print(f"Current Price: {current_price}")
    print(f"Mean Expected Price: {expected_price}")
    print(f"5th Percentile: {percentile_5th}")
    print(f"95th Percentile: {percentile_95th}")
    print(f"Probability of Final Price > Current Price: {probability}")

    # Plot all paths with low opacity to show the range of possible outcomes
    plt.plot(paths, alpha=0.05, color='blue')
    plt.title("Future Price Paths")
    plt.xlabel("Paths")
    plt.ylabel("Prices")
    plt.show()

main()