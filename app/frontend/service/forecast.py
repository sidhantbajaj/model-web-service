import pandas as pd 
import requests 
from datetime import datetime, date
import json
import altair as alt
from constants import HOST_URL, FORECAST_API_ENDPOINT

class ForecastResponse:
    def __init__(self, date: datetime):
        self.date = date.strftime('%Y-%m-%d')

    def convert_response(self, response):
        # Convert the response from the API into a DataFrame.
        raw_data = response.text  # Get raw text from the response
        data_dict = json.loads(raw_data)  # Parse the JSON response into a dictionary
        formatted_data = {date: amount for date, amount in data_dict.items()}  # Format data as key-value pairs
        df = pd.DataFrame(list(formatted_data.items()), columns=['Date', 'Sales($)'])  # Create DataFrame
        df.index += 1  # Start the index at 1 for better presentation
        return df  

    def create_chart(self, df):
        # Create a line chart using Altair to visualize sales over time.
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime format
        chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Date:T', axis=alt.Axis(title='Date', format='%Y-%m-%d', labelAngle=315)),  # X-axis for Date
            y=alt.Y('Sales($):Q', title='Sales ($)'),  # Y-axis for Sales
            tooltip=[alt.Tooltip('Date:T', title='Date', format='%Y-%m-%d'),  # Tooltip for Date
                     alt.Tooltip('Sales($):Q', title='Sales ($)')]  # Tooltip for Sales
        ).properties(
            title='Sales Over Time',  # Chart title
            width=1200,  # Set chart width
            height=500  # Set chart height
        ).configure_title(fontSize=20).configure_axis(
            titleFontSize=18,  # Title font size
            labelFontSize=15  # Label font size
        )
        return chart

    def get_response(self):
        # Make an API call to get sales data for the specified date.
        date = self.date
        api_url = f"{HOST_URL}{FORECAST_API_ENDPOINT}" # API url with backend endpoint
        return requests.get(f"{api_url}?date={date}")  # Return the API response

    def final_response(self):
        # Execute the full response retrieval and data formatting process.
        response = self.get_response()  # Get the response from the API
        formatted_response = self.convert_response(response)  # Convert the response to a DataFrame
        return formatted_response 
