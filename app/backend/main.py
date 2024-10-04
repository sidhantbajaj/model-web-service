# Imports
from fastapi import FastAPI
from service import forecast
from datetime import datetime
from service.forecast import ForecastResults

# Initialize FastAPI app
app = FastAPI()

# Fast API Endpoints
@app.get("/")
def read_root():
    brief = "This project deals with data related to an american retailer that has 10 \
            stores across 3 different states: California (CA), Texas (TX) and Wisconsin (WI). \
            \nProject Objectives:\n1. Conduct Exploratory Data Analysis on datasets for insights.\
            \n2. Apply data pre-processing techniques for cleaned dataset for modelling.\
            \n3. Create two models; one for predicting sales revenue and the other for forecasting.\
            \n4. Create an interactive web application with frontend and backend that generates the results.\
            \n5. Using FastAPI, streamlit and render, create and host the web application.\
            \n\n API Endpoints for reference with respective input parameters:\
            \n1. '/health/' : Returns the status code 200. \
            \n2. '/sales/national/':\
            \n\ti. Input parameters: 'date' in format YYYY-MM-DD. Example - 2016-12-28\
            \n\tii. Ouput format: {""2016-01-01"":10000.01,""2016-01-02"":10001.12,""2016-01-03"":10002.22,""2016-01-04"":10003.30,\
            ""2016-01-05"":10004.46,""2016-01-06"":10005.12,""2016-01-07"":10006.55}\
            \n3. `/sales/stores/items/`: \
            \n\ti. Input parameters: First is 'date' in format YYYY-MM-DD, Example - 2016-12-28. Second is 'store_id', Example - CA_1. \
            Third is 'item_id', Example - HOBBIES_1_001. \
            \n\tii. Output format:{""prediction"":19.72}\
            \n\nGithub repo link - https://github.com/sidhantbajaj/model-web-service.git"
    return brief

# Health Endpoint
@app.get("/health", status_code=200)
def healthcheck():
    return 'Application is all ready to go!'

@app.get("/sales/national/")
def forecast_response(date: str):
    forecast = ForecastResults(date)
    return forecast.result()

