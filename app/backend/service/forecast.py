from starlette.responses import JSONResponse
from datetime import datetime
from joblib import load
import pandas as pd
from constants import FORECAST_MODEL_PATH, DAYS_TO_FORECAST
import numpy as np
np.float_ = np.float64
from prophet import Prophet

class ForecastResults:
    def __init__(self, date: str):
        # Initialize with a specific date, parsed from string format.
        self.date = datetime.strptime(date, '%Y-%m-%d')

    def load_model(self):
        # Load the forecasting model from the specified path.
        return load(FORECAST_MODEL_PATH)

    def get_future_dates(self):
        # Generate a DataFrame containing future dates based on the specified date.
        specific_date = self.date
        future_dates = pd.date_range(specific_date, periods=DAYS_TO_FORECAST, freq='D')
        return pd.DataFrame(future_dates, columns=['ds'])

    def forecast_response(self, model, dates_df):
        # Use the forecasting model to predict future values and format the results.
        forecast = model.predict(dates_df)
        result_df = forecast[['ds', 'yhat']]
        result_df['ds'] = result_df['ds'].dt.strftime('%Y-%m-%d')  # Format the date as 'YYYY-MM-DD'
        result_dict = result_df.set_index('ds')['yhat'].round(2).to_dict()  # Convert to dictionary
        return JSONResponse(result_dict)  # Return the result as a JSON response

    def result(self):
        # Load the model, get future dates, and return the forecast results.
        model = self.load_model()
        future_dates = self.get_future_dates()
        return self.forecast_response(model, future_dates)