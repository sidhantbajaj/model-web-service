import streamlit as st
import datetime
from service.forecast import ForecastResponse
from service.predict import PredictionResponse
from service.brief import BriefResponse
from service.read_json import ReadJSON
from constants import JSON_FILE_PATH


def home_page():
    st.title('Sales Revenue Forecasting and Prediction App')
    st.write("## Welcome to the Home Page!")
    st.write("To know more about this app press the button below")
    if st.button("App Description"):
        response = BriefResponse()
        st.write(response.get_response())
    st.write("## Use the navigation sidebar to access forecast and prediction features")

def prediction_page():
    # Section for sales prediction.
    st.title("Sales Prediction Page")
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
        st.markdown("""
        <div style="text-align: center;">
        <span style="font-size: 24px; font-weight: bold;">Predicted Value ($)</span><br>
        <span style="font-size: 40px;">{}</span>
        </div>
         """.format(prediction_value), unsafe_allow_html=True)  # Display the predicted value as a metric.

def forecast_page():
    st.title("Forecasting Page")
    # Provide a description of the forecasting section.
    st.write('This section aims to provide the total sales revenue forecast for the next 7 days across all the stores')

    # Date input for selecting the forecast date.
    d = st.date_input('Select date for forecast (next 7 days)', value=datetime.date(2019, 7, 6))

    # Button to trigger sales revenue forecasting.
    if st.button("Forecast Sales Revenue"):
        forecast = ForecastResponse(d)  # Create a ForecastResponse object with the selected date.
        response_df = forecast.final_response()  # Get the forecasted sales data.

        st.dataframe(response_df, width=1000)  # Display the sales forecast as a DataFrame.
    
        st.write("""## Line Graph""")
        st.write('This chart shows sales revenue over forecasted dates.')
        st.altair_chart(forecast.create_chart(response_df), use_container_width=True)  # Create and display the forecast chart.

def about_page():
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

# Add a sidebar for navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.selectbox("Go to", ["Home", "Sales Prediction", "Sales Forecast", "About"])

# Display the selected page
if page_selection == "Home":
    home_page()
elif page_selection == "Sales Prediction":
    prediction_page()
elif page_selection == "Sales Forecast":
    forecast_page()
elif page_selection == "About":
    about_page()