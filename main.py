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
    sp = spotipy.Spotify(auth=tokenReadTracks)
    sp = sp.artist(idArtist)
    genres.append(sp['genres'])
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
    # Luego se agrega todos los generos a una lista
    cleanGenre = list(set(allgenre))
    with open(f'myGenres.json', "w") as jsonFile:
        # Se guarda en un .json todos los generos que hay
        jsonFile.write(json.dumps(cleanGenre))
    return(cleanGenre)
    
    

def getTracks(era):    
    songs = []
    eras = []
    # Busca todas las canciones que hay en los me gusta del usuario
    for times in range(22):
        # El numero depende completamente de la cantidad de canciones que hay
        # Para calcular el numero (22) se necesita dividir por 50 la cantidad de canciones

        try:
            # Se hace un try por las dudas si se ingreso mas de la cantidad de canciones que hay
            sp = spotipy.Spotify(auth=tokenReadTracks)
            sp = sp.current_user_saved_tracks(limit=50, offset=times*50)['items']
            # El limite es cuantas canciones se agarran a la vez
            # El offset es el salto que hace
            # En este caso, le digo q haga un salto de 50xtimes, asi puedo agarrar todas las canciones
            for song in range(len(sp)):
            # Por cada cancion que hay agrega el id de la misma, de su artista a una lista
            # Los generos que tiene ese artista y el año del disco
                songs.append({ 'songID': sp[song]['track']['id'], 'artistID': sp[song]['track']['artists'][0]['id'],
                # El 'year' se consigue agarrando el 'release_date' del album (2022-05-05), para despues eliminar los - y conseguir unicamente el año
                # Luego con el len(), se consigue agarrar el anteultimo digitos del año (2) y se le suma 0, para asi quedar como una decada
                'year': ((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0"
                , 'genres': getGenreArtists(sp[song]['track']['artists'][0]['id']), "songName":  sp[song]['track']['name']})
                eras.append(((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0")
                print("Procesando: " + sp[song]['track']['name'] + " El año es: " + ((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0")
        except:
            print("limite")

    with open(f'songs.json', "w") as jsonFile:
        # Se guardan todas las canciones en un .json
        jsonFile.write(json.dumps(songs))
    with open(f'era.json', "w") as jsonFile:
        # Se guardan todas las eras en un .json
        jsonFile.write(json.dumps(eras))
    if era == False:
        # Si se esta haciendo playlists de generos
        createPlaylist(cleanGenres(genres))
        # Se envia a que se limpie la lista de generos y que se creen las playlists
        addSongs(era, songs)
    else:
        createPlaylist(eras)
        addSongs(era, songs)


def createPlaylist(genres):
    # Se crean las playlists de acuerdo a la lista de generos que se le manda
    # En el caso de que sean epocas en vez de generos, funciona igual
    file = open('myPlaylists.json', encoding= "utf8")
    # Se trae la informacion completa de todas las playlists, esto se hace asi 
    # debido a que puede ser que hayan playlists preexistentes de estos generos
    playlistData = json.load(file)

    for genre in genres:
        foundIt = False
        # Por cada genero en la lista de generos
        while foundIt == False:
            # Mientras que no se encuentre una playlists que ya exista con ese nombre
            for playlist in playlistData:
                # Se intenta con cada playlists fijarse si se llama igual
                if playlist['name'] == genre:
                    # Si lo es termina el while
                    foundIt = True
                    break
                else:
                    # Si no lo es, sigue pasando el while
                    pass
            if foundIt == False:
                # Si se termino el for y no se encontro, se crea una playlist de ese genero
                sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                sp = sp.user_playlist_create('gaandrade117' ,genre, public=True)
                # Se guarda la informacion de la nueva creada playlist
                playlistData.append({'id': sp['id'], 'name': sp['name']})
                print("se hizo " + sp['name'])
                break
            else:
                # Si se termino y se encontro, sigue con el siguiente genero
                pass

    with open(f'myPlaylists.json', "w") as jsonFile:
        # Se guarda la actualizada informacion de las playlists
        jsonFile.write(json.dumps(playlistData))
    return(playlistData)


def addSongs(era, songs):
    # Agrega canciones a las playlists
    file = open('myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    numSong = 0
    if era == False:
        # Si se hace pro genero
        for song in songs:
            numSong=+1
            # Por cada cancion que hay fijarse sus generos y buscar la playlist para
            # ese genero, despues averiguar si ya esta dentro de la playlist, si no, agregarse
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
                                # Por cada cancion que ya existe, se compara para ver si es la misma
                                print(numSong +": se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + genre)
                                if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                                    print("ya existe: " + song['songName'])
                                    # Si ya existe, entonces se termina el while y no se agrega
                                    exist = True
                                    break
                            if exist == False:
                                    # Si se termino el for y no se encontro, se agrega la cancion
                                    try:
                                        # Intenta agregar la cancion a la playlist
                                        listaInnecesaria = []
                                        pID = playlist['id']
                                        sID = song['songID']
                                        listaInnecesaria.append(sID)
                                        # Se tiene que hacer una lista, debido a que asi lo pide la API
                                        # En teoria se podria enviar varios items (canciones) a la vez, 
                                        # pero en este programa solo se manda de a uno
                                        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                                        sp = sp.playlist_add_items(pID, listaInnecesaria)
                                        print("Se agrego: " + song['songName'] + " a " + playlist['name'])
                                        exist = True
                                    except:
                                        print("No se pudo agregar: " + song['songName'] + " a " + playlist['name'])
                                        exist = True
    else:
        # En el caso que sea por decada, en vez de por genero
        for song in songs:
                numSong=+1

            # Por cada cancion que hay fijarse su epoca y buscar la playlist para
            # esa epoca, despues averiguar si ya esta dentro de la playlist, si no, agregarse
                for playlist in data:
                    # Por cada playlist en la lista de playlists
                    if song['year'] == playlist['name']:
                        # Si hay una playlist con el nombre del año
                        exist = False
                        while exist == False:
                            sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                            sp = sp.playlist_items(playlist['id'])['items']
                            # Se fija en todas las canciones de la playlist a ver si ya esta
                            for alreadyExistingSong in range(len(sp)):
                                print(numSong +": se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + song['year'])
                                if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                                    print("ya existe: " + song['songName'])
                                    # Si ya existe, entonces se termina el while y no se agrega
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
    # En el caso de estar testeando y querer eliminar varias playlists a la vez
    for playList in data:
        # Por cada playlists que hay, se elimina
        print("eliminando: " + playList['name'])
        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
        sp = sp.user_playlist_unfollow(myID, playList['id'])

getTracks(True)
# True si se quiere hacer por decada
# False si se quiere hacer por genero

