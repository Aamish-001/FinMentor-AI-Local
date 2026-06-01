import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import time
import matplotlib.dates as mdates # Import for date formatting

# Import cross-module functions
import setup
from setup import save_feedback # Keep this as it saves to local CSV

def train_market_model(company):
    """Downloads stock history and trains a Random Forest model for financial forecasting"""
    try:
        # Downloads 1 month of stock records cleanly via yfinance API
        data = yf.download(company, period="1mo", interval="1d", auto_adjust=True, progress=False)
    except Exception as e:
        print(f"\n[Data Error]: Could not fetch company records: {e}")
        return None, None
        
    if data is None or data.empty:
        print("\n[Data Error]: Empty response from ticker registry.")
        return None, None
        
    # Standardize data structure to prevent MultiIndex errors in newer versions of yfinance
    if isinstance(data.columns, __import__('pandas').MultiIndex):
        data.columns = data.columns.droplevel(1)

    # Machine Learning Alignment: Shift records to establish inputs and labels
    data['Prediction'] = data['Close'].shift(-1)
    X = np.array(data[['Close']][:-1])
    y = np.array(data['Prediction'][:-1])
    
    # Instantiate and fit the Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, data

def evaluate_market():
    """Takes input for standard ticker symbols and outputs a textual AI prediction statement"""
    print("\n" + "="*40)
    print("         MARKET PREDICTOR MODULE       ")
    print("="*40)
    
    company = input("Enter Company Ticker (e.g., AAPL, INFY.NS): ").strip().upper()
    if not company:
        print("Cancelled.")
        time.sleep(1.5)
        return

    print(f"\nAnalyzing stock patterns and processing AI model for {company}...")
    model, data = train_market_model(company)
    
    if model is None:
        print("Prediction process halted due to data extraction failure.")
        time.sleep(2.0)
        return
        
    # Extract structural pricing and issue model inference
    latest = float(data['Close'].iloc[-1])
    predicted = model.predict(np.array([[latest]]))[0]
    direction = "UP" if predicted > latest else "DOWN"

    # Currency formatting wrapper (Converts international tags to INR format standard)
    latest_inr = latest if company.endswith(".NS") else latest * 88.0
    predicted_inr = predicted if company.endswith(".NS") else predicted * 88.0

    time.sleep(1.5)
    output_msg = f"The market profile looks to go {direction}!"
    
    print("\n" + "-"*40)
    print(f"RESULTS FOR {company}:")
    print(f"Current Closing Value : ₹{round(latest_inr, 2)}")
    print(f"AI Predicted Next Step: ₹{round(predicted_inr, 2)}")
    print(f"Predicted Trend        : {output_msg}")
    print("-"*40)

    # Automatically save user activity to local log system
    save_feedback([time.strftime("%Y-%m-%d %H:%M:%S"), company, latest_inr, predicted_inr, direction])

    # Displaying Visual Data Visualization Plots (The Graph Part)
    print("\nOpening trend visualization chart window... (Close the chart window to return to app menu)")
    plt.figure(figsize=(9, 5))
    prices = data['Close'] if company.endswith(".NS") else data['Close'] * 88.0
    plt.plot(prices.index, prices.values, label="Historical Trend (INR)", color="#3c96ff", linewidth=2, marker='o')
    plt.axhline(y=predicted_inr, color="#ff3c3c", linestyle="--", label=f"AI Forecast: ₹{round(predicted_inr, 2)}")
    plt.title(f"FinMentor AI - {company} Historical Pricing & Next-Day Prediction Plot")
    plt.xlabel("Timeline History")
    plt.ylabel("Value Base (₹)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    
    # --- START: Changes for date formatting ---
    ax = plt.gca() # Get current axes
    # Set a more compact date format (e.g., Month-Day)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Moved to after xticks rotation
    # --- END: Changes for date formatting ---
    
    plt.show()  # Pauses execution cleanly until graph window is closed by the user

    # Reading Delay: Gives user a 4-second breath window after viewing output and graphs
    print("\nReturning to control menu dashboard...")
    time.sleep(4.0)