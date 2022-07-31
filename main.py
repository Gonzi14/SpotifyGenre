from urllib import response
import requests
import json
import spotipy

urlPlaylist = 'https://api.spotify.com/v1/users/gaandrade117/playlists'
tokenCreatePlaylist = ''
tokenReadTracks = ''
urlTracks = 'https://api.spotify.com/v1/me/tracks'

def getGenreArtists(idsArtists):
    # Se busca los generos de los artistas
    allArtistsjson = {}
    genres = []
    for ids in idsArtists:
        sp = spotipy.Spotify(auth=tokenReadTracks)
        sp = sp.artist(ids)
        genres.append(sp['genres'])
        allArtistsjson[ids] = sp
    # Por cada cancion se agrega los generos a una lista
    print(genres)
    # Se guarda todos los artistas que hay
    with open(f'artistas.json', "w") as jsonFile:
        jsonFile.write(json.dumps(allArtistsjson))

def getTracks():
    # Busca todas las canciones que hay en los me gusta del usuario
    sp = spotipy.Spotify(auth=tokenReadTracks)
    sp = sp.current_user_saved_tracks(limit=10, offset=0)['items']
    ids = []
    idsArtists= []
    for song in range(len(sp)):
        # Por cada cancion que hay agrega el id de la misma y de su artista a dos listas diferentes
        ids.append(sp[song]['track']['id'])
        idsArtists.append(sp[song]['track']['artists'][0]['id'])
    getGenreArtists(idsArtists)
    # Guarda la data de todas las canciones
    with open(f'songs.json', "w") as jsonFile:
        jsonFile.write(json.dumps(sp))

def createPlaylist():
    # Crea una playlist
    response = requests.post(
        urlPlaylist,
        headers= {"Authorization": f"Bearer {tokenCreatePlaylist}"},
        json= {"name": "Genero",
            "public": False}
    )
    jsonResp = response.json()
    print(jsonResp)


getTracks()
