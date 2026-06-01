# LOANADVISOR.PY
from sklearn.linear_model import LogisticRegression
import numpy as np
import math
import time

def train_loan_model():
    """Trains a simple Logistic Regression Machine Learning model to evaluate loans"""
    X = np.array([
        # [Monthly Income, Loan Amount, Interest Rate, Duration (Months)]
        
        # --- GOOD PROFILES (Approved = 1) ---
        [90000, 300000, 9, 60],    # High income, reasonable loan, long tenure (Low EMI)
        [120000, 400000, 10, 48],  # Very high income, handles a 4L loan easily
        [60000, 150000, 8, 36],    # Decent income, modest loan request
        [80000, 200000, 9, 24],    # Strong income relative to a small loan length
        [45000, 100000, 10, 36],   # Lower income but asking for a tiny loan
        
        # --- HIGH RISK PROFILES (Denied = 0) ---
        [25000, 500000, 11, 12],   # CRITICAL: Low income asking for 5L to pay in just 1 year!
        [30000, 350000, 10, 24],   # Loan is too high for a 30k monthly salary
        [15000, 90000, 12, 12],    # Extremely low income, high interest burden
        [50000, 600000, 9, 36],    # Income cannot support a 6L loan over 3 years
        [20000, 150000, 10, 12]    # EMI would completely exceed monthly earnings
    ])
    
    # 1 = Approved, 0 = Denied
    y = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]  
    
    m = LogisticRegression(max_iter=500)
    m.fit(X, y)
    return m

# Train the model globally when file loads
loan_model = train_loan_model()

def loan_predictor(income, loan, annual_rate, months):
    """Calculates the EMI and uses a combined ML model + Financial DTI rule to issue a clear recommendation"""
    # 1. Mathematical EMI calculation formula
    r = (annual_rate / 12) / 100
    emi = (loan * r * math.pow(1 + r, months)) / (math.pow(1 + r, months) - 1)

    # 2. Calculate the Debt-to-Income (DTI) Ratio percentage
    dti_ratio = (emi / income) * 100

    # 3. Use Machine Learning to predict status
    user_data = np.array([[income, loan, annual_rate, months]])
    ml_prediction = loan_model.predict(user_data)[0]

    # 4. Generate the Final Combined Recommendation Strategy
    print("\n" + "------------------------------------------")
    print("FINANCIAL ADVISORY ANALYSIS:")
    print(f"Calculated Monthly EMI: ₹{round(emi, 2)}")
    print(f"EMI-to-Income Ratio    : {round(dti_ratio, 1)}% of your monthly earnings")
    
    # Check if the loan is viable
    if ml_prediction == 1 and dti_ratio <= 45.0:
        msg = (
            f"RECOMMENDATION: SHOULD YOU TAKE THIS LOAN? -> YES ✅.\n"
            f"Reasoning: The machine learning model approves your risk profile, and your monthly EMI "
            f"takes up a safe proportion ({round(dti_ratio, 1)}%) of your income. It is financially sustainable."
        )
    elif ml_prediction == 1 and dti_ratio > 45.0:
        msg = (
            f"RECOMMENDATION: SHOULD YOU TAKE THIS LOAN? -> NO ❌ (PROCEED WITH EXTREME CAUTION).\n"
            f"Reasoning: Even though our ML risk algorithm approves your structural background, your EMI "
            f"would consume {round(dti_ratio, 1)}% of your monthly earnings. This exceeds the safe 45% threshold "
            f"and could cause a severe personal cash-flow crunch."
        )
    else:
        msg = (
            f"RECOMMENDATION: SHOULD YOU TAKE THIS LOAN? -> NO ❌\n"
            f"Reasoning: The system has classified your application as high-risk. This asset structure "
            f"presents a high probability of debt distress or default based on historical profile patterns."
        )

    time.sleep(1.5)
    return msg

def evaluate_loan():
    """Handles text input interface for loan calculations"""
    print()
    print("========================================")
    print("           LOAN ADVISOR MODULE          ")
    print("========================================")
    
    try:
        income = float(input("Enter Monthly Income (₹): "))
        loan = float(input("Enter Desired Loan Amount (₹): "))
        rate = float(input("Enter Annual Interest Rate (%): "))
        months = float(input("Enter Duration in Months: "))
        
        if income <= 0 or loan <= 0 or rate <= 0 or months <= 0:
            print("\nError: Please enter valid values greater than 0.")
            time.sleep(2.0)
            return
            
        # Run prediction and print results
        result = loan_predictor(income, loan, rate, months)
        print("\n" + "--------------------------------------")
        print(result)
        print("-"*40)
        
        # Requested Delay: 4 seconds reading delay for evaluation output
        print("\nReturning to control menu dashboard...")
        time.sleep(4.0)
        
    except ValueError:
        print("\nError: Please type valid numerical numbers.")
        time.sleep(2.0)