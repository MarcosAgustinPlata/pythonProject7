import yfinance as yf
import pandas as pd
import numpy as np

# Sustituye esta lista con los tickers reales de las empresas del CAC 40
tickers = ["AC.PA", "AIR.PA", "AI.PA", "MT.AS", "ATO.PA", "CS.PA", "BNP.PA", "EN.PA",
           "CAP.PA", "CA.PA", "SGO.PA", "ACA.PA", "BN.PA", "DSY.PA", "ENGI.PA", "EL.PA",
           "RMS.PA", "KER.PA", "LR.PA", "OR.PA", "MC.PA", "ML.PA", "ORA.PA", "RI.PA",
           "PUB.PA", "RNO.PA", "SAF.PA", "SAN.PA", "SU.PA", "GLE.PA"] # Completa con todos los tickers

def calculate_metrics(ticker):
    data = yf.download(ticker)
    data['Returns'] = data['Adj Close'].pct_change()
    annual_return = data['Returns'].mean() * 252
    annual_volatility = data['Returns'].std() * np.sqrt(252)
    rolling_max = data['Adj Close'].cummax()
    daily_drawdown = data['Adj Close']/rolling_max - 1.0
    max_drawdown = daily_drawdown.min()
    return ticker, annual_return, annual_volatility, max_drawdown

results = []

for ticker in tickers:
    try:
        results.append(calculate_metrics(ticker))
    except Exception as e:
        print(f"Error downloading or calculating metrics for {ticker}: {e}")

results_df = pd.DataFrame(results, columns=['Ticker', 'Annual Return', 'Annual Volatility', 'Max Drawdown'])
print(results_df)
