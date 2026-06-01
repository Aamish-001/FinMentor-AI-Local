Markdown
# FinMentor AI - Local ML Terminal

This program predicts stock market trends and evaluates credit loan eligibility.

## Features
* **Market Trend Forecaster:** Downloads real-time market records via Yahoo Finance and trains a Random Forest Regressor to predict next-day pricing targets.
* **Loan Eligibility Advisor:** Evaluates credit risks using Logistic Regression model and a 45% Debt-to-Income (DTI) safety ceiling.
* **Voice-Assisted UI:** Integrates local text-to-speech audio narration in the beginning of the program.

##  Local Setup Instructions

Follow these quick steps to run this project on your machine:

Download the github repository.

Set up a local Virtual Environment (Recommended):
python -m venv myenv
Activate it on Windows: myenv\Scripts\activate

Activate it on Mac/Linux: source myenv/bin/activate

Install the required libraries:
pip install numpy yfinance scikit-learn matplotlib pyttsx3 pandas

Launch the application core:
python Main.py

License
This project is licensed under the MIT License.
