import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Step 1: Picking the Stocks ---
# I picked the top 50ish companies in the S&P 500 to get a good feel for the market.
# These are the heavy hitters that usually drive the index.
tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "UNH", "JNJ",
    "XOM", "V", "PG", "HD", "JPM", "MA", "CVX", "ABBV", "MRK", "PEP",
    "KO", "LLY", "BAC", "AVGO", "TMO", "COST", "DIS", "MCD", "CSCO", "ACN",
    "WMT", "ABT", "DHR", "LIN", "NKE", "NEE", "TXN", "VZ", "RTX", "PM",
    "ADBE", "NFLX", "AMD", "ORCL", "CRM", "INTC", "QCOM", "IBM", "HON", "CAT"
]

# Adding SPY (the S&P 500 ETF) so I have something to compare everything else to.
# I need this later to calculate Beta.
tickers.append("SPY") 

print(f"Acquiring data for {len(tickers)} assets...")

# --- Step 2: Grabbing the Data ---
# Downloading 1 year of history so I have enough data points for the stats to actually mean something.
# Doing this all in one big download request so it's faster and I don't annoy the API.
data = yf.download(tickers, period="1y", progress=True)['Close']

# Cleaning up: dropping any columns that are empty so they don't break my math later.
data = data.dropna(axis=1)

# Splitting the data: SPY is my benchmark, everything else is what I'm analyzing.
spy_data = data['SPY']
stock_data = data.drop('SPY', axis=1)

# --- Step 3: The Math (Crunching the Numbers) ---

# A. Simple Moving Average (SMA)
# Calculating the 50-day average. This is my baseline for the "Trend".
sma_50 = stock_data.rolling(window=50).mean()
current_price = stock_data.iloc[-1]
current_sma = sma_50.iloc[-1]

# Checking how far the current price is from that 50-day average.
# If it's positive, we're in a Bull trend. Negative means Bear trend.
dist_sma = ((current_price - current_sma) / current_sma) * 100

# B. Volatility (Risk)
# First, get the daily percent changes.
daily_returns = stock_data.pct_change()
# Then calculate volatility. I'm multiplying by sqrt(252) because there are ~252 trading days in a year.
# This tells me how "shaky" or wild the stock price is.
volatility = daily_returns.std() * np.sqrt(252) * 100

# C. Beta (Market Sensitivity)
# Now figuring out Beta. This tells me if the stock moves with the market or does its own thing.
spy_returns = spy_data.pct_change()
betas = []

# I have to loop through each stock here to compare it against SPY individually.
for ticker in stock_data.columns:
    # Beta formula: Covariance of stock & market / Variance of market
    cov = daily_returns[ticker].cov(spy_returns)
    var = spy_returns.var()
    beta = cov / var
    betas.append(beta)

# Putting all these stats into one nice DataFrame so I can plot it.
metrics = pd.DataFrame({
    'Ticker': stock_data.columns,
    'Distance_SMA': dist_sma.values,
    'Volatility': volatility.values,
    'Beta': betas
}).set_index('Ticker')

# --- Step 4: Visualizing the Results ---
plt.style.use('dark_background') # Dark mode looks way cooler
fig = plt.figure(figsize=(16, 10))
grid = plt.GridSpec(2, 2, hspace=0.3, wspace=0.2)

# Panel 1: The Vibe Check (Breadth)
# A simple pie chart to see if the market is mostly winning (Bullish) or losing (Bearish).
ax1 = fig.add_subplot(grid[0, 0])
bullish_count = (metrics['Distance_SMA'] > 0).sum()
total_count = len(metrics)
bearish_count = total_count - bullish_count

labels = [f'Bullish ({bullish_count})', f'Bearish ({bearish_count})']
colors = ['#00ff00', '#ff0000'] # Green for good, Red for bad
ax1.pie([bullish_count, bearish_count], labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax1.add_artist(plt.Circle((0,0), 0.70, fc='black')) # Turning it into a donut chart
ax1.set_title("Market Regime (Breadth)", fontsize=14, color='white')

# Panel 2: How Strong is the Trend?
# A histogram to show where most stocks are sitting relative to their average.
ax2 = fig.add_subplot(grid[0, 1])
sns.histplot(metrics['Distance_SMA'], bins=20, kde=True, ax=ax2, color='cyan')
ax2.axvline(0, color='white', linestyle='--')
ax2.set_title("Trend Strength Distribution", fontsize=14, color='white')
ax2.set_xlabel("% Distance from 50 SMA")

# Panel 3: The Risk Map (Putting it all together)
# X-Axis: Beta (How much it reacts to the market)
# Y-Axis: Trend (How well it's doing)
# Bubble Size: Volatility (How risky/wild it is)
ax3 = fig.add_subplot(grid[1, :]) # Taking up the whole bottom row

marker_colors = ['#00ff00' if x > 0 else '#ff0000' for x in metrics['Distance_SMA']]
sizes = metrics['Volatility'] * 10 # Making the bubbles big enough to actually see

scatter = ax3.scatter(
    x=metrics['Beta'], 
    y=metrics['Distance_SMA'], 
    s=sizes, 
    c=marker_colors, 
    alpha=0.7, 
    edgecolors='white'
)

# Labeling the outliers so I know which stocks are the crazy ones.
for i, txt in enumerate(metrics.index):
    # Only labeling if the Beta is huge or the trend is super strong
    if abs(metrics['Distance_SMA'][i]) > 15 or metrics['Beta'][i] > 1.5:
        ax3.annotate(txt, (metrics['Beta'][i], metrics['Distance_SMA'][i]), fontsize=9, color='yellow')

ax3.axhline(0, color='white', linestyle='--', alpha=0.5)
ax3.axvline(1, color='white', linestyle='--', alpha=0.5) # Beta of 1 means it moves exactly like the market
ax3.set_xlabel("Beta (Market Sensitivity)", fontsize=12)
ax3.set_ylabel("% Distance from SMA (Trend)", fontsize=12)
ax3.set_title("Risk Map: Beta vs. Trend Strength (Size = Volatility)", fontsize=14, color='white')

plt.tight_layout()
plt.show()

# Printing out the "Hidden Gems" - stocks that are going up but aren't super volatile.
print("\nStrong Trend / Low Volatility Candidates:")
print(metrics[(metrics['Distance_SMA'] > 5) & (metrics['Volatility'] < 25)].sort_values(by='Distance_SMA', ascending=False).head(5))