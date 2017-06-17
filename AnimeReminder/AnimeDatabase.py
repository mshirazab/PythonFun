import os
from Anime import Anime
import pyrebase


class AnimeDatabase(object):
    def __init__(self):
        config = {
            "apiKey": "AIzaSyB9d_59kRrx8NT7e6BO9obmmCT12eKgnuc",
            "authDomain": "animereminder-9bcf0.firebaseapp.com",
            "databaseURL": "https://animereminder-9bcf0.firebaseio.com/",
            "storageBucket": "animereminder-9bcf0.appspot.com",
            "serviceAccount": "/home/shiraz/Programs/AnimeReminder/animereminder-9bcf0-firebase-adminsdk-clody-fa0a506e8f.json"
        }
        FIREBASE = pyrebase.initialize_app(config=config)
        self.__db = FIREBASE.database()

    def add(self, animeName, wikiUrls, gogoUrls):
        anime = Anime(animeName=animeName,
                      wikiUrls=wikiUrls,
                      gogoUrls=gogoUrls)
        self.__db.child('anime').push(anime.getAnimeDictionary())

    def delete(self, animeName):
        key = self.__getKey(animeName)
        if key != 'Not Found':
            self.__db.child('anime').child(key).remove()

    def __getKey(self, animeName):
        try:
            keys = self.__db.child('anime').get().val().keys()
            values = self.__db.child('anime').get().val().values()
            for i in range(len(values)):
                if values[i]['Name'] == animeName:
                    return keys[i]
            return 'Not Found'
        except AttributeError:
            return 'Not Found'

    def update(self, animeName, wikiUrls, gogoUrls):
        self.delete(animeName=animeName)
        self.add(animeName, wikiUrls, gogoUrls)

    def getAll(self):
        try:
            print "Getting All Anime Names from Database"
            values = self.__db.child('anime').get().val()
            print "DONE"
            animes = []
            values = values.values()
            for value in values:
                anime = Anime(animeName=value['Name'],
                              wikiUrls=value['WikiURLs'],
                              gogoUrls=value['GogoURLs'])
                animes.append(anime)
            return animes
        except AttributeError:
            return 'Not Found'
