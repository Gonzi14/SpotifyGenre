from urllib import response
from flask import Flask
import requests
import json
import spotipy

tokenCreatePlaylist = 'BQD008kusU3v9A3L_agMvma-W4pqe7GHWeVUhgP4PxMjTRLMuUu1EsH4dJvO3upFxQXqOO6DdruC27ZIetcP9OIpNzCetknTYt-tQu7T28YkHKy670_C80faJ_0wr7M2B_fpM0zceBgbVJi7-ZUl9je5r_Y3zW3IZJvHcnc8la0LeGJEe5Ml8Ssyxjbkr5ON89z50LliEOQTuBzw0xCS9yqSVX69gUDQjDwJ0xJ0rwgeXuI'
tokenReadTracks= 'BQDztkNZ5kLEY9G56uOXTBmLKURjV3SxKa_gSirYV_SyBtJ0t93LcHsvIvN5hyLaMwSQLMDLg_RkcASPU5fLyQsxTxNCrTDx3MoxCKHyDkP9rnKqORo5d-vQS11D3haxeD9Hs7akuczhnRDXG7WBpf1DRuDs73ZxlL3fReWvfeEK5kdddYwChT7u45VlVGA'
#tokenGetGenre = 'BQB4yGdTD2hLzs1jpqW0x4LWXyRHaQ7LARgyswtddlbMN6FEBBlirzjLmUtPED_3P0UkhV8-G52OWXgMFWb_Bi76gV00z-wMZ7O_QGgK9ZY-rEAnAeYpa9Wp_A1pxuoUCveV6gdl9WJGLB2l8Yp3vhV8IvYETdDQLt1LYuar6xPvfM8CvA'
myID= ""
#token = spotipy.util.prompt_for_user_token("gaandrade117", scope="user-library-read playlist-modify-public")
genres = []
def getGenreArtists(idArtist):
    # Se busca los generos de los artistas
    #print("artist : "+ idArtist)
    sp = spotipy.Spotify(auth=tokenReadTracks)
    sp = sp.artist(idArtist)
    genres.append(sp['genres'])
    #allArtistsjson[ids] = sp
    # Por cada cancion se agrega los generos a una lista
    return (sp['genres'])

def cleanGenres(genres):
    allgenre = []
    for item in genres:
        # Elimina las listas de generos dentro de los generos
        if isinstance(item, list):
            for item2 in item:
                allgenre.append(item2)
        else:
            allgenre.append(item)
    cleanGenre = list(set(allgenre))
    with open(f'myGenres.json', "w") as jsonFile:
        jsonFile.write(json.dumps(cleanGenre))
    # Elimina la repeticion de generos 
    return(cleanGenre)
  
    # Se guarda todos los artistas que hay
    
    

def getTracks():    
    songs = []
    # Busca todas las canciones que hay en los me gusta del usuario
    for times in range(1):
        #22
        try:
            sp = spotipy.Spotify(auth=tokenReadTracks)
            sp = sp.current_user_saved_tracks(limit=1, offset=times*50)['items']
    
            for song in range(len(sp)):
                # Por cada cancion que hay agrega el id de la misma y de su artista a una lista
                songs.append({ 'songID': sp[song]['track']['id'], 'artistID': sp[song]['track']['artists'][0]['id'], 'genres': getGenreArtists(sp[song]['track']['artists'][0]['id']), "songName":  sp[song]['track']['name']})
        except:
            print("limite")
    with open(f'songs.json', "w") as jsonFile:

        jsonFile.write(json.dumps(songs))
    #print(songs)
    createPlaylist(cleanGenres(genres))
    addSongs(songs)
    # Guarda la data de todas las canciones
def createPlaylist(genres):
    file = open('myPlaylists.json', encoding= "utf8")
    playlistData = json.load(file)
    for genre in genres:
        foundIt = False
        while foundIt == False:
            for playlist in playlistData:
                # Por cada playlist que hay, se fija si su nombre es igual al genero
                if playlist['name'] == genre:
                    # Si lo es termian el while
                    foundIt = True
                    break
                else:
                    # Si no lo es, sigue pasando el while
                    pass
            if foundIt == False:
                # Si se termino el for y no se encontro, se crea una playlist de ese genero
                sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                sp = sp.user_playlist_create('gaandrade117' ,genre, public=True)
                playlistData.append({'id': sp['id'], 'name': sp['name']})
                print("ya esta hecho " + sp['name'])
                break
            else:
                # Si se termino y se encontro, sigue con el siguiente genero
                pass
    with open(f'myPlaylists.json', "w") as jsonFile:
        jsonFile.write(json.dumps(playlistData))
    return(playlistData)
    # Crea una playlist


def addSongs(songs):
    file = open('myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    for song in songs:
        #print(song)
        # Por cada cancion que hay fijarse sus generos y fijarse si hay una playlist para
        # Ese genero, si no lo hay, crearla y agregarlo, si l hay simpelmente gregarlo
        #print(song['genres'])
        for genre in song['genres']:
            # Por cada genero en la cancion
            for playlist in data:
                # Por cada playlist en la lista de playlists
                if genre == playlist['name']:
                    # Si hay una playlist con el nombre del genero
                    exist = False
                    while exist == False:
                        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                        sp = sp.playlist_items(playlist['id'])['items']
                        # Se fija en todas las canciones de la playlist a ver si ya esta
                        for alreadyExistingSong in range(len(sp)):
                            print("se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + genre)
                            if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                                print("ya existe: " + song['songName'])
                                # Si ya exisate, entonces se termina el while y no se agrega
                                exist = True
                                break
                        if exist == False:
                                # Si se termino el for y no se encontro, se agrega la cancion
                                try:

                                    listaInnecesaria = []
                                    pID = playlist['id']
                                    sID = song['songID']
                                    listaInnecesaria.append(sID)
                                    sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                                    sp = sp.playlist_add_items(pID, listaInnecesaria)
                                    print("Se agrego: " + song['songName'] + " a " + playlist['name'])
                                    exist = True
                                except:
                                    print("No se pudo agregar: " + song['songName'] + " a " + playlist['name'])
                                    exist = True

def deletePlaylist(data):
    for playList in data:
        print("eliminando: " + playList['name'])
        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
        sp = sp.user_playlist_unfollow(myID, playList['id'])
    
getTracks()
#listGenre()