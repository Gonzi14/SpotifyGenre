import json
from traceback import print_tb
from unicodedata import name
import spotipy
import sys
from math import ceil
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import date


tokenCreatePlaylist = 'BQB3xeOfoSz-0FhHz9qoaQ8vEsTFnX9Y1qnP0sspcCK9hyjjgV-IOtPrnz4vnROrlW_l4h5X3zrpWAGi2wHfwhnn3NaRZZUgtCJbvzxTo9XMOltseW8x4uowrBg5ViK0yso8k45K9f6fBhCxQZHZwTAAnxcH5gCq3TmSHGWhpMwo6Y6jwTAJbnFbnCaruhzU1uQWUaMZFADn8bizOjbHE2xWJ6q4KEerAQAhYAky6nMbY1s'
tokenReadTracks= 'BQAjULij455w025hQp26baLLYjd0hkgelG4xxbFqSklBzuNm-2TPNsQWhgxui4UItvum2yTRnPFWqjcdl3CjdaWcUXhD0QYR9xjw5GJFlBMbg9vtrISzOngBuJgoAKVC0sfmeGCMpJy2gdU97GwXOBREONFqQFwomHzZJdznv3TSBu56aWSIzgT9I-GwgzU'
tokenTop = 'BQAsrFhptZrOnt-_lCvEqpqVQdgfloSZPWC5NVtfgTsLMmPXalxamD-nOXJxjoWLa-uqgmRn4wPslDKyyPQiqzzACQuAQ7X6awQsRW3rrWKlTxtnUIzPnXu0bkMDo0wuZ8Jawnwpb4G961Rns5pMpNqjzEZRA_mCo-t3PEBsQSCJ4raf0M3yUXpA8A'
genres = []
rounds =ceil(int(sys.argv[1])/50)
noGenrePlaylist = None

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
    dfGenres = pd.DataFrame(cleanGenre)
    dfGenres.to_csv('Genres.csv', index=False)
    with open(f'myGenres.json', "w") as jsonFile:
        # Se guarda en un .json todos los generos que hay
        jsonFile.write(json.dumps(cleanGenre))
    return(cleanGenre)

def getTracks(rounds):    
    songs = []
    eras = []
    num = 0
    # Busca todas las canciones que hay en los me gusta del usuario
    for times in range(rounds):
        
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
                num=num+1
            # Por cada cancion que hay agrega el id de la misma, de su artista a una lista
            # Los generos que tiene ese artista y el año del disco
                songs.append({"songName":  sp[song]['track']['name'],'artistName': sp[song]['track']['artists'][0]['name'],'songID': sp[song]['track']['id'], 'artistID': sp[song]['track']['artists'][0]['id'],
                # El 'year' se consigue agarrando el 'release_date' del album (2022-05-05), para despues eliminar los - y conseguir unicamente el año
                # Luego con el len(), se consigue agarrar el anteultimo digitos del año (2) y se le suma 0, para asi quedar como una decada
                'year': ((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0"
                , 'genres': getGenreArtists(sp[song]['track']['artists'][0]['id'])})
                eras.append(((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0")
                print(str(num) + ": Procesando: " + sp[song]['track']['name'])
        except:
            print("limite")
    dfSongs = pd.DataFrame(songs)
    dfSongs.to_csv('Songs.csv', index=False)
    with open(f'songs.json', "w") as jsonFile:
        # Se guardan todas las canciones en un .json
        jsonFile.write(json.dumps(songs))
    with open(f'eras.json', "w") as jsonFile:
        # Se guardan todas las eras en un .json
        jsonFile.write(json.dumps(eras))
    dfEras = pd.DataFrame(eras)
    dfEras.to_csv('Eras.csv', index=False)
    createPlaylist(cleanGenres(genres))
    createPlaylist(eras)
    addSongs(songs, noGenrePlaylist)

def createNoGenrePlaylist():
    file = open('myPlaylists.json', encoding= "utf8")
    foundIt = False
    # Se trae la informacion completa de todas las playlists, esto se hace asi 
    # debido a que puede ser que exista ya la sin genero
    playlistData = json.load(file)
    while foundIt == False:
            # Mientras que no se encuentre la playlist
            for playlist in playlistData:
                # Se intenta con cada playlists fijarse si se llama igual
                if playlist['name'] == "NoGenre":
                    # Si lo es termina el while
                    
                    foundIt = True
                    return playlist
                else:
                    # Si no lo es, sigue pasando el while
                    pass
            if foundIt == False:
                # Si se termino el for y no se encontro, se crea la playlist
                sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                sp = sp.user_playlist_create('gaandrade117' ,"NoGenre", public=True)
                # Se guarda la informacion de la nueva creada playlist
                playlistData.append({'id': sp['id'], 'name': sp['name']})
                print("se hizo " + sp['name'])
                dfPlaylists = pd.DataFrame(playlistData)
                dfPlaylists.to_csv('Playlists.csv', index=False)
                print(dfPlaylists)
                with open(f'myPlaylists.json', "w") as jsonFile:
                    # Se guarda la actualizada informacion de las playlists
                    jsonFile.write(json.dumps(playlistData))
                return sp

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
                print("se hizo la playlist: " + sp['name'])
                break
            else:
                # Si se termino y se encontro, sigue con el siguiente genero
                pass
    dfPlaylists = pd.DataFrame(playlistData)
    dfPlaylists.to_csv('Playlists.csv', index=False)
    with open(f'myPlaylists.json', "w") as jsonFile:
        # Se guarda la actualizada informacion de las playlists
        jsonFile.write(json.dumps(playlistData))

def addSongs(songs, noGenrePlaylist):
    # Agrega canciones a las playlists
    file = open('myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    num = 0
    for song in songs:
        # Por cada cancion
        num=num+1
        if not song['genres']:
            # Si no tiene generos
            if noGenrePlaylist == None:
                # Se fija si ya esta guardada la info de la playlist sin genero
                noGenrePlaylist = createNoGenrePlaylist()
                
            prueba(song, noGenrePlaylist, num)
        for playlist in data:
            for genre in song['genres']:
                if genre == playlist['name']:
                    # Si hay una playlist con el nombre del genero
                    prueba(song, playlist, num)
            if song['year'] == playlist['name']:
                # Si hay una playlist con el nombre del año
                prueba(song, playlist, num)

def prueba(song,playlist, num):
    exist = False
    while exist == False:
        for times in range(3):
            sp = spotipy.Spotify(auth=tokenCreatePlaylist)
            sp = sp.playlist_items(playlist['id'], limit= 100, offset= times * 100 )['items']
        # Se fija en todas las canciones de la playlist a ver si ya esta
            for alreadyExistingSong in range(len(sp)):
                # Por cada 100 canciones que ya existen, se compara para ver si es la misma
                print(str(num) + "- Se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + playlist['name'])
                if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                    print("ya existe: " + song['songName'] + "en " + playlist['name'])
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

def deletePlaylist(data):
    # En el caso de estar testeando y querer eliminar varias playlists a la vez
    for playList in data:
        # Por cada playlists que hay, se elimina
        print("eliminando: " + playList['name'])
        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
        sp = sp.user_playlist_unfollow(myID, playList['id'])

def createTopPlaylist():
    fecha = date.today()
    types = ['long_term', 'medium_term', 'short_term']
    for Moment in types:
        namePlaylist = (str(fecha) + " " + Moment)
        lista = []
        sp = spotipy.Spotify(auth=tokenTop)
        sp = sp.current_user_top_tracks(20, 0, Moment)['items']
        for song in range(len(sp)):
            lista.append({"songName":  sp[song]['name'],'artistName': sp[song]['artists'][0]['name'],'songID': sp[song]['id'], 'artistID': sp[song]['artists'][0]['id'], 'year': ((sp[song]['album']['release_date']).split("-")[0])[len(((sp[song]['album']['release_date']).split("-")[0]))//2] + "0", 'genres': [Moment]})
        with open(f'pruebaL.json', "w") as jsonFile:
            # Se guarda en un .json todos los generos que hay
            jsonFile.write(json.dumps(lista))
        createPlaylist([namePlaylist])
        addSongs(lista, noGenrePlaylist)

getTracks(rounds)
#createTopPlaylist()
