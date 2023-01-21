# Rainfall_Prediction
Collected the past 30 years of rainfall data for Hyderabad and conducted statistical time series forecasting with a
set of 36 features by using python’s scikit learn, darts and statsmodels packages to find best fit for extreme rainfall
prediction.
Developed a customized data preprocessing toolkit to extract seasonality, trend and extreme rainfall event in
association with Indian Meteorological Department (IMD) for better accessibility.
Studied and compared the MAPE metric of Auto ARIMA, exponential smoothing and T-BATS with modern ML
algorithms such as RNNs, LSTM and N-BEATS to evaluate the best fit.
Based on results, exponential smoothing and LSTM performed best with MAPE under 5% from a baseline of 35%
for a forecast window of 5 years.
