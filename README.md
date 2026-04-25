# quant-trading-strategies

Quantitative Trading Strategy Analysis
A collection of Python-based quantitative trading tools covering strategy backtesting, stochastic simulation, statistical arbitrage, risk analysis, and options pricing.

**Projects**
Crossover Strategy
Backtests a moving average crossover strategy (20-day vs 50-day MA) across 3-year historical data using yfinance. Generates buy/sell signals on MA crossovers, computes cumulative strategy returns, and compares performance against a buy-and-hold benchmark.

Mean Reversion
Implements a Bollinger Band mean reversion strategy using a 20-day rolling Z-score. Enters positions when price deviates beyond ±2σ from the rolling mean and visualises both the Bollinger Bands and Z-score over time.

Pairs Trading
Builds a pairs trading model by computing the rolling price spread between two equities and generating long/short entry signals at ±2σ Z-score thresholds with mean-reversion exit logic at ±0.5σ. Counts total entry and exit signals across a 3-year window.

Monte Carlo Simulation
Simulates 1,000 future price paths over 252 trading days using log-normal returns calibrated from historical mean and standard deviation. Outputs expected price, 5th/95th percentile confidence bounds, and probability of positive return.

Risk Analysis
Computes annualised return, annualised volatility, Sharpe ratio, and maximum drawdown for multiple equities. Ranks assets by risk-adjusted performance and visualises drawdown curves over time.

Options Payoff
Calculates and visualises profit/loss profiles for European call and put options across a range of underlying prices at expiry, with automated break-even computation.

**Tech Stack**
Python — core language
yfinance — historical market data
NumPy — numerical computation and random simulation
pandas — time series manipulation
Matplotlib — data visualisation
