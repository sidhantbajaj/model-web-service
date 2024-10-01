import pandas as pd
import requests
from datetime import datetime, date
import json

class PredictionResponse:
    def __init__(self, date: datetime, store_id: str, item_id: str):
        self.date = date.strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
        self.store_id = store_id  # Store ID
        self.item_id = item_id  # Item ID

    def convert_response(self, response):
        # Convert the API response to extract the prediction value.
        raw_data = response.text  # Get raw text from the response
        data = json.loads(raw_data)  # Parse the JSON response into a dictionary
        return data['prediction']  # Return the prediction value from the response
    
    def get_response(self):
        # Make an API call to retrieve sales prediction for the specified date, store, and item.
        date = self.date  # Get the formatted date
        api_url = "http://172.17.0.2:8000/sales/stores/items/"  # API endpoint
        return requests.get(f"{api_url}?date={date}&store_id={self.store_id}&item_id={self.item_id}")  # Return the API response
    
    def final_response(self):
        # Execute the response retrieval and conversion to get the final prediction result.
        response = self.get_response()  # Get the response from the API
        formatted_response = self.convert_response(response)  # Convert the response to get the prediction
        return formatted_response  # Return the extracted prediction value
