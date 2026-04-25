"""
Options Payoff Calculator
Visualises profit/loss for call and put options across a range of
underlying prices at expiry, with break-even calculation.
"""

import numpy as np
import matplotlib.pyplot as plt

def stock_info():
    """Gather option parameters from user input."""
    strike_price = float(input("Strike Price: "))
    premium = float(input("Premium: "))
    call_put = input("Call or Put: ").lower()

    return strike_price, premium, call_put

def main():

    strike_price, premium, call_put = stock_info()

    # Generate a range of possible stock prices at expiry
    prices = np.linspace(0, 2 * strike_price, 200)

    if call_put == "call":

        # Call payoff: profit when stock price exceeds strike + premium
        call_payoff = np.maximum(prices - strike_price, 0) - premium

        break_even = strike_price + premium
        print(f"Break Even {break_even}")

        plt.plot(prices, call_payoff)
        plt.axhline(y=0, color="black", linestyle="--")
        plt.title(f"Call Payoff | Strike: {strike_price} | Premium: {premium}")
        plt.xlabel("Stock Price at Expiry")
        plt.ylabel("Profit/Loss")
        plt.show()


    elif call_put == "put":
        # Put payoff: profit when stock price falls below strike - premium
        put_payoff = np.maximum(strike_price - prices, 0) - premium

        break_even = strike_price - premium
        print(f"Break Even {break_even}")

        plt.plot(prices, put_payoff)
        plt.axhline(y=0, color="black", linestyle="--")
        plt.title(f"Put Payoff | Strike: {strike_price} | Premium: {premium}")
        plt.xlabel("Stock Price at Expiry")
        plt.ylabel("Profit/Loss")
        plt.show()


main()