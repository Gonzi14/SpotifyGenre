import json
from traceback import print_tb
import spotipy
import sys
from math import ceil
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


tokenCreatePlaylist = 'BQDurTFNTubZw-MoiVMiJGBWnsYeXNqWCethXjFxJc1wIfM97EpaSr_g0ZzJRC_SFrCPJTcwCltOm9PnYAKaOGsc5MfLkB0RHxxSk6cR-V0oDH8OpN8QgtO7PdVCEQn0SgzRnVaQxqRkZk6wzisn_asyWWQpRhVMb6BatgmkBym4UDYXEOnr31n7pTBZ8mRTA6Hh-5D-UcATZuBxMM4CXzMQ0jFGe_VxUD-acnQhOCVImQk'
tokenReadTracks= 'BQA4iX3ATkWs5M6iNd40GRcE2SVfYaTij7ph9JHDqI8SLQg6Q29N0R_aZ25TIF7qMGWgInjq3cFeLLz1FhhvLKz83KGATEWQy6KZtTVqvlgRTyvPuRWpPqKl76I66R0u2zBFxqXxgRsmBl1LOp2aCcQ7AnInjj8w-AAXhk99d9aE0L-oGnE3zV8cI200fGg'
genres = []
myID = ""
era = sys.argv[1] in (True, False)
rounds =ceil(int(sys.argv[2])/50)

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
    print(dfGenres)
    with open(f'myGenres.json', "w") as jsonFile:
        # Se guarda en un .json todos los generos que hay
        jsonFile.write(json.dumps(cleanGenre))
    return(cleanGenre)
    
    

def getTracks(era, rounds):    
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
    print(dfSongs)
    with open(f'songs.json', "w") as jsonFile:
        # Se guardan todas las canciones en un .json
        jsonFile.write(json.dumps(songs))
    with open(f'eras.json', "w") as jsonFile:
        # Se guardan todas las eras en un .json
        jsonFile.write(json.dumps(eras))
    dfEras = pd.DataFrame(eras)
    dfEras.to_csv('Eras.csv', index=False)
    print(dfEras)
    if era == False:
        # Si se esta haciendo playlists de generos
        createPlaylist(cleanGenres(genres))
    else:
        # Se envia a que se limpie la lista de generos y que se creen las playlists
        createPlaylist(eras)
    #addSongs(era, songs)

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
                    return playlist['id']
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
                return(sp['id'])


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
    print(dfPlaylists)
    with open(f'myPlaylists.json', "w") as jsonFile:
        # Se guarda la actualizada informacion de las playlists
        jsonFile.write(json.dumps(playlistData))
    return(playlistData)


def addSongs(era, songs):
    # Agrega canciones a las playlists
    file = open('myPlaylists.json', encoding= "utf8")
    data = json.load(file)
    num = 0
    if era == False:
        # Si se hace por genero
        for song in songs:
            num=num+1
            if not song['genres']:
                
                exist = False
                while exist == False:
                    for times in range(10):
                        # Se hace 1000 veces que son la cantidad maxima posible de canciones en una playlist
                        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                        sp = sp.playlist_items(noGenreID, limit= 100, offset= times * 100 )['items']
                    # Se fija en todas las canciones de la playlist a ver si ya esta
                        for alreadyExistingSong in range(len(sp)):
                            # Por cada 100 canciones que ya existe, se compara para ver si es la misma
                            print(str(num) + "- Se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: NoGenre")
                            if sp[alreadyExistingSong]['track']['id'] == song['songID']:
                                print("ya existe: " + song['songName'])
                                # Si ya existe, entonces se termina el while y no se agrega
                                exist = True
                                break
                    if exist == False:
                    # Si la cancion no tiene genero entonces se agrega a una playlist especial
                        listaInnecesaria = []
                        sID = song['songID']
                        listaInnecesaria.append(sID)
                        sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                        sp = sp.playlist_add_items(noGenreID, listaInnecesaria)
                        print("Se agrego: " + song['songName'] + " a la lista random")
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
                            for times in range(10):
                                sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                                sp = sp.playlist_items(playlist['id'], limit= 100, offset= times * 100 )['items']
                            # Se fija en todas las canciones de la playlist a ver si ya esta
                                for alreadyExistingSong in range(len(sp)):
                                    # Por cada 100 canciones que ya existen, se compara para ver si es la misma
                                    print(str(num) + "- Se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + genre)
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
                num=num+1
            # Por cada cancion que hay fijarse su epoca y buscar la playlist para
            # esa epoca, despues averiguar si ya esta dentro de la playlist, si no, agregarse
                for playlist in data:
                    # Por cada playlist en la lista de playlists
                    if song['year'] == playlist['name']:
                        # Si hay una playlist con el nombre del año
                        exist = False
                        while exist == False:
                            for times in range(10):
                                sp = spotipy.Spotify(auth=tokenCreatePlaylist)
                                sp = sp.playlist_items(playlist['id'], limit= 100, offset= times * 100 )['items']
                            # Se fija en 100 canciones en la playlist a ver si ya esta
                                for alreadyExistingSong in range(len(sp)):
                                    print(str(num) + "- Se esta comparando " + song['songName'] + " con: " + sp[alreadyExistingSong]['track']['name'] + " que ya esta adentro en: " + song['year'])
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


# True si se quiere hacer por decada
# False si se quiere hacer por genero
noGenreID = createNoGenrePlaylist()
getTracks(era, rounds)