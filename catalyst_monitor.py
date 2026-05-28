import yfinance as yf

# Define your high-volatility watchlist
target_tickers = ['IONS', 'RCAT', 'EVGO', 'SIDU']

def run_catalyst_monitor(tickers):
    print("Initializing Catalyst Monitor...\n")
    
    for ticker_symbol in tickers:
        stock = yf.Ticker(ticker_symbol)
        news_data = stock.news
        
        # Check if there is recent news available
        if news_data:
            latest_news = news_data[0]
            title = latest_news.get('title', 'No Title')
            link = latest_news.get('link', 'No Link')
            publisher = latest_news.get('publisher', 'Unknown')
            
            print(f"[{ticker_symbol}] - SOURCE: {publisher}")
            print(f"HEADLINE: {title}")
            print(f"LINK: {link}\n")
        else:
            print(f"[{ticker_symbol}] No recent news catalysts found.\n")

if __name__ == "__main__":
    run_catalyst_monitor(target_tickers)
