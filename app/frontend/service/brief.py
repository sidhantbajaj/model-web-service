import requests
from constants import HOST_URL

class BriefResponse:
    def __init__(self):
        self.host_url = HOST_URL

    def get_response(self):
        api_url = self.host_url 
        response = requests.get(f"{api_url}/") # Return the API response
        return response.text