import requests
import json

class TaskHelper:
    # Next time use os to read env vars instead storing them here.
    BASE_URL = "XXXXX"
    API_KEY = "XXXXX"
    OPENAI_API_KEY = "XXXXXX"

    def __init__(self):
        self.base_url = TaskHelper.BASE_URL
        self.api_key = TaskHelper.API_KEY

    def auth(self, task):
        api_endpoint = f"{self.base_url}/token/{task}"

        data = {"apikey": self.api_key}
        response = requests.post(api_endpoint, json.dumps(data))
        jsonResponse = response.json()

        return jsonResponse.get("token")

    def get_task(self, token, debug=False):
        api_endpoint = f"{self.base_url}/task/{token}"

        response = requests.get(api_endpoint)
        if debug:
            print(response.json())

        return response.json()

    def send_task(self, token, answer):
        api_endpoint = f"{self.base_url}/answer/{token}"

        data = {"answer": answer}
        response = requests.post(api_endpoint, json.dumps(data))
        print(response.json())
