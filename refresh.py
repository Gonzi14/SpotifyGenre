import json
import requests

id64 =  # myID base64

page = "https://accounts.spotify.com/authorize?client_id=43e2c4f5542f44ba99cff85ab3f149bb&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2FGonzi14%2FSpotifyGenre&scope=playlist-modify-public%20playlist-modify-private%20user-library-read%20user-top-read%20user-read-currently-playing" 

code = "AQAq_UJ9FbbddXDsg1Hs_yFCRZbs1I6FKvtajHuNzZVAq6rDM0nH7R3Lj4Fu3-9yjoLSOz834pdujc7YjMayqt0d7TXzW2rwKL910JFdWwrJJz1xPX5n6mQa4kbqeZJezgd0vLh9a2r19VeQQgTkGJpbpnpFJIny9TFrJgXuVlZaFUYzjbpu1bEgBmuOxa9R22DtpJRb9QOsH6k-OwgaWUanCyhIe9x3gacrboPrkIvP4un5wugaKN06zNAbVpdO3MwcXrLG5Ey0deR6rvSPT9gQIlIAVO-AlptCTJYZiSaqvzq-pBKdyW3R9iWNFMl7HkvURQWyMlomUdU"

# curl -H "Authorization: Basic NDNlMmM0ZjU1NDJmNDRiYTk5Y2ZmODVhYjNmMTQ5YmI6MzFmM2Y1ZTA0NDQyNDRiYjlkZGZmZjRkOTMyZTgzZTA=" -d grant_type=authorization_code -d code=AQAq_UJ9FbbddXDsg1Hs_yFCRZbs1I6FKvtajHuNzZVAq6rDM0nH7R3Lj4Fu3-9yjoLSOz834pdujc7YjMayqt0d7TXzW2rwKL910JFdWwrJJz1xPX5n6mQa4kbqeZJezgd0vLh9a2r19VeQQgTkGJpbpnpFJIny9TFrJgXuVlZaFUYzjbpu1bEgBmuOxa9R22DtpJRb9QOsH6k-OwgaWUanCyhIe9x3gacrboPrkIvP4un5wugaKN06zNAbVpdO3MwcXrLG5Ey0deR6rvSPT9gQIlIAVO-AlptCTJYZiSaqvzq-pBKdyW3R9iWNFMl7HkvURQWyMlomUdU -d redirect_uri=https%3A%2F%2Fgithub.com%2FGonzi14%2FSpotifyGenre https://accounts.spotify.com/api/token

respuestaTest = {"access_token":"BQAWYWwgbtvXNpAdcvgyFJT3vljUw25gxWxHvqO57IJSOB1om868wILiCJOxGLE9i-IZlK6KtFefqh4lYrkFCTh_MFyJbBcdW_x3k5zj-En3MCNgLeaoG_Iek-IkcZq5u4twAjyzYqYWl0D3XGef4bY1-2IjhIMNx7O6cV-gK-Cso7W9T2wmkdvXbdTPicXe5DhEgDhphNTb8EjOo4dVjZiwsgFrrxyEcXr25MbWo2_3kZSL91LQQb1KUVI6Nbww8S8Z","token_type":"Bearer","expires_in":3600,"refresh_token":"AQDbiHKEFGU1psmiPxgEsWM3SpfJ-0V94y-e6ZyQlGF2B2Pi00DDGS61GmECJD3YZx0vabD5BsJDEw3O4D0JyTW_k24f0XAmwOJYqMm-qeP5TsJOFJhL67eCJUI4Hlxkj60","scope":"user-library-read playlist-modify-private playlist-modify-public user-read-currently-playing user-top-read"}

refresh_token = "AQDbiHKEFGU1psmiPxgEsWM3SpfJ-0V94y-e6ZyQlGF2B2Pi00DDGS61GmECJD3YZx0vabD5BsJDEw3O4D0JyTW_k24f0XAmwOJYqMm-qeP5TsJOFJhL67eCJUI4Hlxkj60"
def refresh():

    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query, data={"grant_type":"refresh_token", "refresh_token":refresh_token}, headers={"Authorization":"Basic " + id64})
    return (response.json()['access_token'])