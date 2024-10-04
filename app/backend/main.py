# Imports
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from service import forecast
from datetime import datetime
from service.forecast import ForecastResults
from service.predict import PredictionResults
from service.brief import BriefResults

# Initialize FastAPI app
app = FastAPI()

# Fast API endpoints
@app.get("/", response_class=PlainTextResponse)
def read_root():
    brief = BriefResults()
    return brief.response()

# Health endpoint
@app.get("/health", status_code=200)
def healthcheck():
    return 'Application is all ready to go!'

# Forecast model endpoint
@app.get("/sales/national/")
def forecast_response(date: str):
    forecast = ForecastResults(date)
    return forecast.result()

@app.get("/sales/stores/items/")
def prediction_response(date: str, store_id: str, item_id: str):
    prediction = PredictionResults(date, store_id, item_id)
    return prediction.result()