#  Market Breadth & Risk Dashboard

This project is a Python-based analytics tool that visualizes the overall health of the S&P 500 using multi-factor risk metrics and trend analysis.

## About This Project
In quantitative finance, "Market Breadth" is a key concept used to judge the quality of a trend. It distinguishes between a healthy market, where participation is broad, and a weak one driven by just a handful of large-cap stocks. To get a better look, this tool analyzes the top 50 holdings of the S&P 500 one by one. It combines three metrics—trend (SMA), risk (Volatility), and market sensitivity (Beta)—to build a 3D risk map of the current market environment.

##  Features
* **Automated Data Retrieval:** Fetches historical price data for the top 50 S&P 500 holdings using Yahoo Finance.

* **Multi-Factor Calculation:** Computes the 50-day SMA, Beta against SPY, and Annualized Volatility for every asset.

* **Regime Detection:** Generates a "Breadth Gauge" to visualize the ratio of Bullish vs. Bearish stocks.

* **Risk Mapping:** Creates a 3D scatter plot (Risk vs. Reward vs. Volatility) to identify safe trends and dangerous outliers.

##  Tech Stack
* **Data Acquisition:** `yfinance` (Vectorized bulk downloads)
* **Data Processing:** `pandas`, `numpy` (Rolling windows, covariance matrices)
* **Visualization:** `matplotlib`, `seaborn` (Statistical plotting)

##  How to Use
# 1. Prerequisites
* Python 3.8+
* Git


# 2. Setup & Installation
Clone this repository and set up the virtual environment:

```bash
# 1. Clone the repository to your local machine
git clone https://github.com/YourUsername/Market-Breadth-Dashboard.git
cd Market-Breadth-Dashboard

# 2. Create a Python virtual environment
python -m venv venv

# 3. Activate the environment
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 4. Install the required libraries
pip install -r requirements.txt

```

# 3. Running the Dashboard
You can customize the asset universe by editing the tickers list at the top of the market_breadth.py file.
```bash
Python

# --- Step 1: Picking the Stocks ---
tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "TSLA", "META", 
    "BRK-B", "UNH", "JNJ", "XOM", "V", "PG", "HD", "JPM"
    # ... Add or remove tickers here
]
```
Once customized, simply run the script from your terminal:
```bash
python dashboard.py
```

##  Core Concepts Applied
* **Vectorization:** Calculating Beta and Volatility for 50+ assets simultaneously without slow loops.
* **Risk Modeling:** Implementing CAPM concepts (Beta) and Statistical Risk (Volatility) in Python.
* **Market Microstructure:** Handling real-world data issues (missing tickers, NaN values, delisted assets).

##  Screenshots
*<img width="1920" height="1015" alt="Dashboard" src="https://github.com/user-attachments/assets/1b77c486-1f38-4f57-a929-914f9a4487ef" />
