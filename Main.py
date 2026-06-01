import sys

# Import cross-module components from your project modules
from setup import speak
import loanAdvisor
import marketPredictor # Our newly separated module

def main_menu():
    """Central operational routing matrix for the console deployment"""
    # Plays voice greeting once at startup outside the menu loop to prevent loop stuttering
    speak("Welcome to FinMentor A I")
    
    while True:
        print("\n" + "="*50)
        print("                  FINMENTOR AI                   ")
        print(" Status: Local Session (Cloud Sync Disabled)")
        print("="*50)
        print("1. Market Trend Forecaster (Machine Learning)")
        print("2. Credit Loan Eligibility Advisor (Machine Learning)")
        print("3. Terminate Core System")
        print("-"*50)
        
        choice = input("Enter operational choice (1-3): ").strip()
        
        if choice == "1":
            marketPredictor.evaluate_market() # Calls separated module route
        elif choice == "2":
            loanAdvisor.evaluate_loan()
        elif choice == "3":
            print("\nShutting down core engine connections. Goodbye!")
            sys.exit()
        else:
            print("\nInvalid operation matrix range selection. Type 1 to 4.")

if __name__ == "__main__":
    main_menu()