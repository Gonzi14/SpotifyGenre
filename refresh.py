import json
import requests

id64 =  # myID base64


def refresh():

    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query, data={"grant_type":"refresh_token", "refresh_token":refresh_token}, headers={"Authorization":"Basic " + id64})
    return (response.json()['access_token'])
