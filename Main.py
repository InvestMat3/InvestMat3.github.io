import yfinance as yf
import pandas as pd
import numpy as np

# Function to calculate financial metrics
def calculate_metrics(tickers):
    metrics = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        
        # Get historical data
        hist = stock.history(period='1y')
        
        # Calculate beta
        beta = stock.info['beta']
        
        # Calculate standard deviation of returns
        returns = hist['Close'].pct_change().dropna()
        std_dev = returns.std()
        
        # Calculate P/E ratio
        pe_ratio = stock.info.get('forwardPE', np.nan)
        
        # Calculate dividend yield
        dividend_yield = stock.info.get('dividendYield', 0) * 100  # Convert to percentage
        
        # Append the metrics to the list
        metrics.append({
            'Ticker': ticker,
            'Beta': beta,
            'Std Dev': std_dev,
            'P/E Ratio': pe_ratio,
            'Dividend Yield (%)': dividend_yield
        })

    return pd.DataFrame(metrics)

# Function to filter stocks based on risk and timeframe
def filter_stocks(df, risk, timeframe):
    if timeframe == 'short-term':
        df = df[(df['Beta'] < 1) & (df['Std Dev'] < 0.05)]
    elif timeframe == 'medium-term':
        df = df[(df['P/E Ratio'] < 20) & (df['Std Dev'] < 0.07)]
    elif timeframe == 'long-term':
        df = df[(df['Dividend Yield (%)'] > 2) & (df['P/E Ratio'] < 25)]

    return df

# Main function
def main():
    # Define your stock tickers
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX']  # Will have to add more/Find a way to look at every stock (possibly every stock in the smp 500 maybe?)
    
    # Get financial metrics
    metrics_df = calculate_metrics(tickers)
    
    # User inputs
    risk = input("Enter your risk preference (low, medium, high): ").strip().lower()
    timeframe = input("Enter your investment timeframe (short-term, medium-term, long-term): ").strip().lower()
    
    # Filter stocks based on user inputs
    filtered_stocks = filter_stocks(metrics_df, risk, timeframe)
    
    print("\nSuggested Stocks:")
    print(filtered_stocks)

if __name__ == "__main__":
    main()
