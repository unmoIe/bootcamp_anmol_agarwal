## Problem Statement
**Predict short term volatility(daily) in the stock market**    
Forecasting daily stock market volatility is essential for portfolio risk management.  
Volatility reflects the degree of variation in stock returns, and sudden spikes can significantly impact portfolio performance.
Predicting short-term volatility is challenging due to market noise, regime changes, and macroeconomic factors.
A reliable predictive model can provide portfolio managers with daily forecasts, enabling timely risk adjustments, efficient capital allocation, and informed trading decisions to improve portfolio expected returns.

## Stakeholder & User
The primary stakeholders are portfolio managers, they can use accurate future volatility estimates to better hedge out their positions, adapt trading strategies, and improve returns for the portfolio.  
They will use the volatility predictions in their existing workflows, allowing them to adjust position sizing, stop-loss levels, and hedges in real-time.   
Decisions based on the predicted volatility will be made before the market opens each day, using the daily predicted volatility, ensuring the forecasts integrate seamlessly with intraday trading strategies.   

## Useful Answer & Decision
This is a predictive model which gives a daily volatility forecast.   
Artifact to deliver is a predictive model written in python, that returns daily volatility of the market and also backtests results on historical data.   

## Assumptions & Constraints
The model assumes that past market behaviour is indicative of the near-term future.   
Real time data availability is a constraint of this model to be able to predict future volatility.   
Demand for computing resources is a constraint.   
The model should have a low latency to ensure as close to real-time volatility prediction as possible.   

## Known/Unknowns Risks
Black swan events or outliers which are tough to predict are a source of known risk.   
Model hyperparameters may require tuning; performance may vary across stocks/sectors.   
Monitoring plan: Compare predicted vs. realized volatility daily; log errors for model refinement.   

## Lifecycle Mapping   
Goal → Stage → Deliverable  
Forecast daily stock volatility → Problem Framing & Scoping (Stage 01) → Deliverable: Project scope document, stakeholder mapping  
Prepare & clean historical data → Data collection and preprocessing → Deliverable: Cleaned dataset and data dictionary  
Build predictive model → Modeling → Deliverable: Python model with predictions  
Validate model performance → Evaluation and Backtesting → Deliverable: Forecast accuracy report, visualization plots.  
Integrate into workflow → Deployment/Artifact Delivery → Deliverable: Reproducible python project with daily forecast outputs.  

## Repo Plan
/data - Raw and cleaned historical stock data  
/src - Python scripts for data processing and modeling  
/notebooks - Jupyter notebooks for exploration, modeling, and backtesting  
/docs - Project documentation, reports, and visualizations  
cadence for updates - Weekly commits for model development; daily updates for results/forecast logs during testing phase.

## Data Storage
- folder structure: data/raw, data/processed
- .csv stored in data/raw, .parquet stored in data/parquet
- I have used parquet file because they take up less space and have fater I/O
- I have used csv because its better for visualization and is readily readable
- Both these files are being saved/read using DATA_DIR_RAW or DATA_DIR_PROCESSED env variables stored in .env

## Cleaning Strategy
Assumption:
- Fill missing data with median: The missing values are missing at random, and median is a good measure of central tendency as its less affected by outliers than the mean.
- Drop missing data: The missing values were again random, and you have enough data left afetr dropping to give some substantial outcome.
- Normalize with min-max scaling: Data is bounded, relative distance between min-max is meaningful.
- Normalize with standard scaling: data is roughly gaussian, and mean/variance are meaningful representation of data
Tradeoffs:
- Fill missing data with median: Robust to outliers but may reduce the variance of data incorrectly.
- Drop missing data: Avoid inducing any bias because there is no addition of data but only when missed dsata is not at random, also prone to losing a lot of data sometimes
- Normalize with min-max scaling: preserves relative distance between data points but extremely sensitive to outliers
- Normalize with standard scaling: handles outliers better than min-max, but still may be sensitive to outliers, also works on the assumption that data is normally distributed