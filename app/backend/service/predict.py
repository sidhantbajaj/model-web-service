import pandas as pd
import numpy as np 
from joblib import load
from datetime import datetime
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from category_encoders import TargetEncoder
import xgboost as xgb
from constants import PREDICTIVE_MODEL_PATH, SCALER_ENCODER, TARGET_MEAN_ENCODER, ORDINAL_ENCODER
from starlette.responses import JSONResponse

class PredictionResults:
    def __init__(self, date: str, store_id: str, item_id: str):
        # Initialize with a specific date, store ID, and item ID, parsing the date.
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.store_id = store_id
        self.item_id = item_id

    def input_data(self):
        # Extract components needed for prediction input.
        date = self.date
        item_id = self.item_id
        
        # Derive department and category IDs from item ID.
        dept_id = "_".join(item_id.split("_")[:2])
        cat_id = dept_id.split("_")[0]

        store_id = self.store_id
        state_id = store_id.split("_")[0]

        # Extract date components.
        day = date.day
        month = date.month
        year = date.year   

        # Create a dictionary for DataFrame input.
        data_dict = {
            "item_id": [item_id],
            "dept_id": [dept_id],
            "cat_id": [cat_id],
            "store_id": [store_id],
            "state_id": [state_id],
            "year": [year],
            "month": [month],
            "day": [day]
        }
        
        # Return the input DataFrame.
        return pd.DataFrame(data_dict)

    def data_transformation(self, df):
        # Load necessary encoders and scalers for data transformation.
        target_mean_encoder = load(TARGET_MEAN_ENCODER)
        ordinal_encoder = load(ORDINAL_ENCODER)
        scaler = load(SCALER_ENCODER)

        # Initialise an empty DataFrame for the encoded data.
        encoded_df = pd.DataFrame()

        # Apply target mean encoding to the DataFrame.
        encoded_df = target_mean_encoder.transform(df)
        
        # Apply ordinal encoding for specified categorical columns.
        encoded_df[['dept_id', 'store_id', 'cat_id', 'state_id']] = ordinal_encoder.transform(
            encoded_df[['dept_id', 'store_id', 'cat_id', 'state_id']])
        
        # Scale the data using the fitted scaler.
        scaled_data = scaler.transform(encoded_df)

        # Return the scaled DataFrame with original columns.
        return pd.DataFrame(scaled_data, columns=encoded_df.columns)

    def load_model(self):
        # Load the predictive model from the specified path.
        return load(PREDICTIVE_MODEL_PATH)

    def prediction_response(self, df):
        # Load model, make prediction, and prepare the response.
        model = self.load_model()
        prediction = model.predict(df)

        # Prepare the result dictionary with the rounded prediction.
        result_dict = {"prediction": round(prediction.tolist()[0], 2)}

        return JSONResponse(result_dict)  # Return the prediction result as JSON.

    def result(self):
        # Execute the prediction pipeline and return the final prediction response.
        input_df = self.input_data()  # Gather input data.
        transformed_df = self.data_transformation(input_df)  # Transform the data.
        return self.prediction_response(transformed_df)  # Get prediction response.
