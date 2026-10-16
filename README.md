
# MarketMind

AI-powered financial risk intelligence using machine learning,
explainable predictions, and portfolio stress testing.

## Current Progress

Day 1: Project setup and historical market-data pipeline.

## Objective

Investigate whether regime-aware machine learning can improve
financial risk assessment across different market conditions.

## Current Features

- Historical NIFTY 50 data collection
- Data validation and duplicate removal
- Local CSV storage
- Interactive historical price dashboard

## Technology Stack

- Python
- Pandas and NumPy
- yfinance
- Scikit-learn
- Streamlit
- Plotly

## Setup

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
python -m pip install -r requirements.txt
python -m src.data_loader
streamlit run app.py
```

## Research Plan

1. Engineer financial risk indicators.
2. Identify market regimes.
3. Train and compare risk-prediction models.
4. Evaluate explanations and prediction reliability.
5. Test portfolio stress scenarios.

## Data and Limitations

Historical market data is obtained from Yahoo Finance via yfinance.
This is an educational research prototype, not investment advice.
Predictions and backtest results will not guarantee future performance.
