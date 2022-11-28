from copyreg import add_extension
import csv
from importlib.machinery import all_suffixes
import json
from winreg import QueryReflectionKey
from platform import platform
from traceback import print_tb
from unicodedata import name
from urllib import response
import spotipy
import sys
from math import ceil
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
from refresh import refresh

clientID = "43e2c4f5542f44ba99cff85ab3f149bb"
secretID = "31f3f5e0444244bb9ddfff4d932e83e0"
token = refresh()
token2 = "BQDmjzrzJOQVCnp316Snq8wGNmmGAQg4Noe7Z8JpJZpyPv6tspRyckVu-uP37VMtxWIx_GM2Z5LtIn2-ZlzoW16i78LljIFSGB5dingfNO_mnFaFy45eFk2CVnlWNaVBbwPBh90yNp4sxOkIV1jCJj_i_ppa7vcAPiXfsqL-vRC_oIIPzg"
genres = []
rounds =ceil(int(sys.argv[1])/50)
noGenrePlaylist = None

def getCurrentTrack():
    sp = spotipy.Spotify(auth="BQBtyg5V8FR8zYyIRYarJiYnSy9DJKNPH-C_OGwglXMaMGq8rmCVyx8FnKNxV_UciJSNkCN9_EaUNHwChaYfoQWm8eSQoUQSd_yEmgh7lmunZ250lBGHGVslTJPPq-3mwd_BqTV6uOfbjWhkqtgxCyWQTZ57H65bXyMuTnGG17M1Kk_dRMk8Yd4")
    sp = sp.current_user_playing_track()
    print(sp)
    return sp

def save(item, name):
    # Para guardar absolutamente cualquier cosa en formato json y csv
    dfitem = pd.DataFrame(item)
    dfitem.to_csv(f"{name}.csv", index=False)
    with open(f"{name}.json", "w") as jsonFile:
        jsonFile.write(json.dumps(item))

def getGenreArtists(idArtist):
    # Se busca los generos de los artistas
    sp = spotipy.Spotify(auth=token2)
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
    return(cleanGenre)

def getTracks(rounds):
    file = open('static/mySongs.json', encoding= "utf8")
    data = json.load(file)
    lenAlreadyKnownSongs = len(data)
    songs = []
    newSongs = []
    eras = []
    num = 0
    # Busca todas las canciones que hay en los me gusta del usuario
    for times in range(rounds):
        
        # El numero depende completamente de la cantidad de canciones que hay
        # Para calcular el numero se necesita dividir por 50 la cantidad de canciones

            sp = spotipy.Spotify(auth=token)
            sp = sp.current_user_saved_tracks(limit=50, offset=times*50)['items']
            # El limite es cuantas canciones se agarran a la vez
            # El offset es el salto que hace
            # En este caso, le digo q haga un salto de 50xtimes, asi puedo agarrar todas las canciones
            for song in range(len(sp)):
                audioSong = audio(sp[song]['track']['id'])
                num=num+1
            # Por cada cancion que hay agrega el id de la misma, de su artista a una lista
            # Los generos que tiene ese artista y el año del disco
                songs.append({"songName":  sp[song]['track']['name'],'artistName': sp[song]['track']['artists'][0]['name'],'songID': sp[song]['track']['id'], 'artistID': sp[song]['track']['artists'][0]['id'],
                # El 'year' se consigue agarrando el 'release_date' del album (2022-05-05), para despues eliminar los - y conseguir unicamente el año
                # Luego con el len(), se consigue agarrar el anteultimo digitos del año (2) y se le suma 0, para asi quedar como una decada
                'year': ((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0"
                ,'disc': sp[song]['track']['album']['name'], 'popularity': sp[song]['track']['popularity'], 'genres': getGenreArtists(sp[song]['track']['artists'][0]['id']),'danceability': audioSong[0], 'energy': audioSong[1], 'key': audioSong[2], 'loudness': audioSong[3], 'speechiness': audioSong[4], 'acousticness': audioSong[5], 'instrumentalness': audioSong[6], 'liveness': audioSong[7], 'valence': audioSong[8], 'tempo': audioSong[9]})
                eras.append(((sp[song]['track']['album']['release_date']).split("-")[0])[len(((sp[song]['track']['album']['release_date']).split("-")[0]))//2] + "0")
                print(str(num) + ": Procesando: " + sp[song]['track']['name'])
                
    
    addedSongs = len(songs) - lenAlreadyKnownSongs
    for g in range(addedSongs):
        newSongs.append(songs[g])
    createPlaylist(cleanGenres(genres))
    createPlaylist(eras)
    save(songs, "mySongs")
    addSongs(newSongs, noGenrePlaylist)
    checkNumSongartists()
    checkNumSongPlaylist()
    
   
def createPlaylist(genres):
    # Se crean las playlists de acuerdo a la lista de generos que se le manda
    file = open('static/myPlaylists.json', encoding= "utf8")
    playlistData = json.load(file)
    # Se trae la informacion completa de todas las playlists, esto se hace asi 
    # debido a que puede ser que hayan playlists preexistentes de estos generos
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
                    playlistAlreadyExisting = {'name': playlist['name'], 'id': playlist['id']}
                else:
                    # Si no lo es, sigue pasando el while
                    pass
            if foundIt == False:
                # Si se termino el for y no se encontro, se crea una playlist de ese genero
                sp = spotipy.Spotify(auth=token)
                sp = sp.user_playlist_create('gaandrade117' ,genre, public=True)
                # Se guarda la informacion de la nueva creada playlist
                playlistData.append({'id': sp['id'], 'name': sp['name']})
                print("se hizo la playlist: " + sp['name'])
                save(playlistData, "myPlaylists")
                return sp
            else:
                # Si se termino y se encontro, sigue con el siguiente genero
                pass
        return playlistAlreadyExisting
    

def addSongs(songs, noGenrePlaylist):
    # Agrega canciones a las playlists
    file = open('static/myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    num = 0
    for song in songs:
        # Por cada cancion
        num=num+1
        if not song['genres']:
            # Si no tiene generos
            if noGenrePlaylist == None:
                # Se fija si ya esta guardada la playlists de los sin generos
                noGenrePlaylist = createPlaylist(['NoGenre'])
                
            prueba(song, noGenrePlaylist, num)
        for playlist in data:
            for genre in song['genres']:
                if genre == playlist['name']:
                    # Si hay una playlist con el nombre del genero
                    prueba(song, playlist, num)
            if song['year'] == playlist['name']:
                # Si hay una playlist con el nombre del año
                prueba(song, playlist, num)
            if song['artistName'] == playlist['name']:
                prueba(song, playlist, num)

def prueba(song,playlist, num):
    # En base a una cancion que se quiere agregar a una plalist
    exist = False
    while exist == False:
        for times in range(4):
            sp = spotipy.Spotify(auth=token)
            sp = sp.playlist_items(playlist['id'], limit= 100, offset= times * 100 )['items']
            # Se fija en todas las canciones de la playlist a ver si ya esta
            print(str(num) + "- Se esta comparando " + song['songName'] + " en " + playlist['name'])
            for alreadyExistingSong in range(len(sp)):
                # Por cada 100 canciones que ya existen, se compara para ver si es la misma
                if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                    print("ya existe: " + song['songName'] + " en " + playlist['name'])
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
                    sp = spotipy.Spotify(auth=token)
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
        sp = spotipy.Spotify(auth=token)
        sp = sp.user_playlist_unfollow(myID, playList['id'])

def createTopPlaylist():
    # No esta terminado todavia
    # Crea el top de canciones de terminos
    fecha = date.today()
    types = ['long_term', 'medium_term', 'short_term']
    for Moment in types:
        namePlaylist = (str(fecha) + " " + Moment)
        lista = []
        sp = spotipy.Spotify(auth=token)
        sp = sp.current_user_top_tracks(20, 0, Moment)['items']
        for song in range(len(sp)):
            lista.append({"songName":  sp[song]['name'],'artistName': sp[song]['artists'][0]['name'],'songID': sp[song]['id'], 'artistID': sp[song]['artists'][0]['id'], 'year': ((sp[song]['album']['release_date']).split("-")[0])[len(((sp[song]['album']['release_date']).split("-")[0]))//2] + "0", 'genres': [Moment]})
        with open(f'pruebaL.json', "w") as jsonFile:
            # Se guarda en un json todos los generos que hay
            jsonFile.write(json.dumps(lista))
        createPlaylist([namePlaylist])
        addSongs(lista, noGenrePlaylist)

def checkNumSongPlaylist():
    # Averigua cuantas canciones hay en una playlist
    allPlaylists = []
    file = open('static/myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    for playlist in data:
        songs = 0
        for times in range(3):
            sp = spotipy.Spotify(auth=token)
            sp = sp.playlist_items(playlist['id'], limit= 100, offset= times * 100 )['items']
            songs = songs + len(sp)
        allPlaylists.append({'id': playlist['id'], 'name': playlist['name'], 'songs' : songs})
        
    save(allPlaylists, "static/myPlaylists")

def checkNumSongartists():
    listArtists = []
    artistsNumSongs = []
    file = open('static/mySongs.json', encoding= "utf8")
    data = json.load(file)
    for song in range(len(data)):
        num = 0
        artist = {'name': data[song]['artistName'], 'id': data[song]['artistID'],'numSongs': None}
        if artist not in listArtists:
            # Si el artista todavia no esta en la lista se lo agrega
            listArtists.append(artist)
            # Se agrega a la lista de nunmeros de canciones tambien
            artistsNumSongs.append({'name': data[song]['artistName'], 'numSongs': 1})
        else:
            # Si el artista ya esta,entonces se le quiere decir qe hay una cancion adicional en la cual aparece
            for alreadyIn in listArtists:
                # Por cada cancion que ya esta en la lista de artistas
                if alreadyIn == artist:
                    # Si se encuentra una igualdad, se le agrega una cancion a ese artista
                    artistsNumSongs[num]['numSongs'] = artistsNumSongs[num]['numSongs'] + 1
                num = num + 1
    num = 0
    for artist in listArtists:
        #Por cada artista que hay, se le cambia el numero de canciones que tiene, por el correcto
        artist['numSongs'] = artistsNumSongs[num]['numSongs']
        num = num + 1
        if artist['numSongs'] >= 5:
            # Si hay mas de 5 canciones, se le crea una playlist
            createPlaylist([artist['name']])
            searchSongs(artist['name'])
    save(listArtists, "myArtists")

def audio(id):
    # Averigua los datos sobre el audio de una cancion
    features = []
    alreadyList = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    sp = spotipy.Spotify(auth=token)
    sp = sp.audio_features(id)[0]
    for each in alreadyList:
        features.append(sp[each])
    return features
            
def average():
    # Genera el promedio de todas las canciones
    file = open('static/mySongs.json', encoding= "utf8")
    data = json.load(file)
    list = {'danceability': 0, 'energy': 0, 'key': 0, 'loudness': 0, 'speechiness': 0, 'acousticness': 0, 'instrumentalness': 0, 'liveness': 0, 'valence': 0, 'tempo': 0}
    for song in data:
        for item in list:
            list[item] = list[item] + song['audio'][0][item]
    for item in list:
        list[item] = list[item]/len(data)
    return list

def bar(): 
    file = open('static/mySongs.json', encoding= "utf8")
    data = json.load(file)
    # Hace los graficos de las canciones
    fig, ax = plt.subplots()
    df = pd.DataFrame(data)
    df.plot(subplots = True,y=['energy', 'danceability', 'speechiness', 'acousticness'], ax=ax, legend=True)
    plt.show()
    fig, ax = plt.subplots()
    df.plot(subplots = True, y=['instrumentalness', 'liveness', 'energy', 'valence'], ax=ax, legend=True)
    plt.show()
    fig, ax = plt.subplots()
    df.plot(subplots = True, y=['key', 'loudness', 'tempo'], ax=ax, legend=True)
    plt.show()

def searchSongs(filter):
    file = open('static/mySongs.json', encoding= "utf8")
    data = json.load(file)
    for song in data:
        if filter == song['artistName']:
            print(song['artistName'])
            prueba(song, createPlaylist([filter]), 14)

getTracks(rounds)
#bar()
#createTopPlaylist()
#getCurrentTrack()