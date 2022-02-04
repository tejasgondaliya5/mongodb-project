import requests
import json


def get_room_id():
    url = "https://video.trukyn.com/get-token"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = eval(response.text)
    if response:
        url = "https://video.trukyn.com/create-meeting"

        payload = json.dumps({
            "token": response["token"]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = eval(response.text)
        return response
    

