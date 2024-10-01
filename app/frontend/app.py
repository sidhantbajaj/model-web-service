import streamlit as st
import datetime
from service.forecast import ForecastResponse
from service.predict import PredictionResponse
from service.read_json import ReadJSON
from constants import JSON_FILE_PATH

st.title('Sales Revenue Forecasting and Prediction App')

st.write("""
## App Description

Utilising the data collected by an American retail store from stores in California, Texas, and Wisconsin, this application aims to provide 
forecasting and prediction for the sales revenue.

## API Endpoints

/: Brief description of the project. 

/health/: Returns a welcome message with status code 200.

/sales/national/: Forecasts the next 7 days sales revenue of all the stores based on input date (YYYY-MM-DD).

/sales/stores/items/: Predicts sales revenue for an item in a store on a specific date.

## Github Repository
""")

st.markdown("[Click here to visit the repository](https://github.com/sidhantbajaj/model-web-service)")

st.write("""## Forecasting""")

# Provide a description of the forecasting section.
st.write('This section aims to provide the total sales revenue forecast for the next 7 days across all the stores')

# Date input for selecting the forecast date.
d = st.date_input('Select date for forecast (next 7 days)', value=datetime.date(2019, 7, 6))

# Button to trigger sales revenue forecasting.
if st.button("Forecast Sales Revenue"):
    forecast = ForecastResponse(d)  # Create a ForecastResponse object with the selected date.
    response_df = forecast.final_response()  # Get the forecasted sales data.
    
    st.write("Sales Table")
    st.dataframe(response_df, width=1000)  # Display the sales forecast as a DataFrame.
    
    st.write("""## Line Graph""")
    st.write('This chart shows sales revenue over forecasted dates.')
    st.altair_chart(forecast.create_chart(response_df), use_container_width=True)  # Create and display the forecast chart.

# Section for sales prediction.
st.write("""## Prediction""")
st.write('This section aims to provide the sales revenue prediction for an item sold in a store on a single date')

# Date input for selecting the prediction date.
date = st.date_input('Select prediction date', value=datetime.date(2019, 7, 6))

# Dropdown for selecting the store ID.
store_id = st.selectbox("Type/Select the store_id for prediction", ("CA_1", "CA_2", "CA_3", "CA_4", 
                                                                  "TX_1", "TX_2", "TX_3", 
                                                                  "WI_1", "WI_2", "WI_3"))

# Read item IDs from JSON file.
item_id_file = ReadJSON(JSON_FILE_PATH)
item_id = st.selectbox("Type/Select the item_id for prediction", item_id_file.json_to_list())  # Dropdown for selecting item ID.

# Button to trigger sales revenue prediction.
if st.button("Predict Sales Revenue"):
    prediction = PredictionResponse(date, store_id, item_id)  # Create a PredictionResponse object with inputs.
    prediction_value = prediction.final_response()  # Get the predicted sales value.
    
    st.metric(label="Predicted Value ($)", value=prediction_value)  # Display the predicted value as a metric.

