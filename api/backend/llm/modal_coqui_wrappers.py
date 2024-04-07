from os import environ
import requests
import json

def text_to_speech(text: str, emotion: str, speed: float):
    # send a request to api
    token = environ["MODAL_AUTH_TOKEN"]
    url = "https://harrolee--tts-api-fastapi-app.modal.run/tts"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "emotion": emotion,
        "speed": f"{speed}"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except requests.exceptions.Timeout:
        print("modal is probaby idle. Write logic here to try again in 22 seconds.")
    except requests.exceptions.ConnectionError:
        print("connection error. handle this appropriately")
    
    if response.status_code == 200:
        return response.content
    print(f"response code was {response.status_code} for url {url}")
    raise SystemExit