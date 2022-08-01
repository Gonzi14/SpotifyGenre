from urllib import response
import requests
import json
import spotipy

urlPlaylist = 'https://api.spotify.com/v1/users/gaandrade117/playlists'
tokenCreatePlaylist = ''
tokenReadTracks = ''
urlTracks = 'https://api.spotify.com/v1/me/tracks'
myID= "43e2c4f5542f44ba99cff85ab3f149bb"

def getGenreArtists(songs):
    # Se busca los generos de los artistas
    allArtistsjson = {}
    genres = []
    for ids in songs:
        print(ids['artistID'])
        sp = spotipy.Spotify(auth=tokenReadTracks)
        sp = sp.artist(ids['artistID'])
        genres.append(sp['genres'])
        #allArtistsjson[ids] = sp
    # Por cada cancion se agrega los generos a una lista
    allgenre = []
    for item in genres:
        # Elimina las listas de generos dentro de los generos
        if isinstance(item, list):
            for item2 in item:
                allgenre.append(item2)
        else:
            allgenre.append(item)
    cleanGenre = list(set(allgenre))
    # Elimina la repeticion de generos 
    print(cleanGenre)
    createPlaylist(cleanGenre)
    # Se guarda todos los artistas que hay
    with open(f'artistas.json', "w") as jsonFile:
        jsonFile.write(json.dumps(allArtistsjson))

def getTracks():
    songs = []
    # Busca todas las canciones que hay en los me gusta del usuario
    for times in range(1):
        #22
        try:
            sp = spotipy.Spotify(auth=tokenReadTracks)
            sp = sp.current_user_saved_tracks(limit=10, offset=times*50)['items']
    
            for song in range(len(sp)):
                # Por cada cancion que hay agrega el id de la misma y de su artista a una lista
                songs.append({ 'songID': sp[song]['track']['id'], 'artistID': sp[song]['track']['artists'][0]['id']})
        except:
            print("limite")
    with open(f'songs.json', "w") as jsonFile:

        jsonFile.write(json.dumps(songs))
    print(songs)
    getGenreArtists(songs)
    # Guarda la data de todas las canciones
    

def createPlaylist(genres):
    # Crea una playlist
    for genre in genres:
        response = requests.post(
            urlPlaylist,
            headers= {"Authorization": f"Bearer {tokenCreatePlaylist}"},
            json= {"name": genre,
                "public": False}
        )
        jsonResp = response.json()
        id = jsonResp['id']
        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
        sp = sp.user_playlist_unfollow(myID, id)
    


getTracks()