import yfinance as yf
import pandas as pd
from datetime import datetime

# Define your short squeeze watchlist
squeeze_targets = ['BEEM', 'SMR', 'NKLA']
mission_data = []

print("Gathering Short Interest Intelligence...")

for ticker in squeeze_targets:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Extract short interest metrics
    short_pct = info.get('shortPercentOfFloat', 'N/A')
    
    # Format the percentage if data is available
    if short_pct != 'N/A' and short_pct is not None:
        short_pct = f"{round(short_pct * 100, 2)}%"
        
    mission_data.append({
        'Date_Logged': datetime.now().strftime("%Y-%m-%d"),
        'Ticker': ticker,
        'Short_Percent_of_Float': short_pct,
        'Total_Shares_Short': info.get('sharesShort', 'N/A'),
        'Days_To_Cover': info.get('shortRatio', 'N/A')
    })

# Convert to a DataFrame and export to CSV
df = pd.DataFrame(mission_data)
output_filename = "short_interest_tracker.csv"
df.to_csv(output_filename, index=False)

print(f"Mission complete. Data exported to {output_filename}.")
