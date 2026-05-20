from fastapi import FastAPI, BackgroundTasks
import threading
import time
import random
import uvicorn

app = FastAPI()

# Global State Variables
system_active = False
portfolio = [
    {"ticker": "AAPL", "qty": 10, "average_cost": 150.00, "current_price": 145.00},
    {"ticker": "NVDA", "qty": 5, "average_cost": 800.00, "current_price": 820.00}
]
activity_logs = ["System Initialized. Awaiting Command."]

# --- 1. AI & Trading Engines ---

def execute_trade(action: str, ticker: str):
    log = f"[{action}] Executed for {ticker}"
    activity_logs.insert(0, log) # Add to top of logs
    print(log)

def risk_manager_loop():
    while True:
        if system_active:
            for pos in portfolio:
                # Mock real-time price update
                pos['current_price'] = pos['current_price'] * random.uniform(0.98, 1.02) 
                
                percent_change = ((pos['current_price'] - pos['average_cost']) / pos['average_cost']) * 100
                if percent_change <= -5.0:
                    execute_trade("EMERGENCY SELL (Stop-Loss)", pos['ticker'])
                    portfolio.remove(pos) # Remove from portfolio after selling
        time.sleep(5)

def market_scanner_loop():
    universe = ["MSFT", "TSLA", "AMZN", "GOOGL"]
    while True:
        if system_active:
            ticker = random.choice(universe)
            # Mock MFI + Bollinger strategy detection
            found_setup = random.choice([True, False, False, False, False])
            if found_setup:
                execute_trade("BUY (MFI+BB Setup)", ticker)
        time.sleep(10)

# --- 2. FastAPI Endpoints (For Android App) ---

@app.get("/api/status")
def get_status():
    return {"active": system_active, "logs": activity_logs[:5]}

@app.get("/api/portfolio")
def get_portfolio():
    return {"portfolio": portfolio}

@app.post("/api/command/{command}")
def send_command(command: str):
    global system_active
    if command == "start":
        system_active = True
        activity_logs.insert(0, "AI Trading Engines: ONLINE")
    elif command == "stop":
        system_active = False
        activity_logs.insert(0, "AI Trading Engines: OFFLINE (Halted)")
    return {"active": system_active}

# --- 3. Server Startup ---
if __name__ == "__main__":
    # Start AI threads in the background
    threading.Thread(target=risk_manager_loop, daemon=True).start()
    threading.Thread(target=market_scanner_loop, daemon=True).start()
    
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
