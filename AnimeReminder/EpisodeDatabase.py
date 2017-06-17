from Episode import Episode
import pyrebase
import os

class EpisodeDatabase(object):
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

    def add(self, anime):
        episode = Episode(anime)
        self.__db.child(anime.animeName).push(episode.getEpisodeDictionary())

    def delete(self, animeName):
        print "Deleting EpisodeList of " + animeName
        key = self.__getKey(animeName)
        if key != 'Not Found':
            self.__db.child(animeName).remove()

    def __getKey(self, animeName):
        try:
            dictionaries = self.__db.child(animeName).get().val()
            keys = dictionaries.keys()
            values = dictionaries.values()
            for i in range(len(values)):
                if values[i]['Name'] == animeName:
                    return keys[i]
            return 'Not Found'
        except AttributeError:
            return 'Not Found'

    def update(self, anime):
        self.delete(animeName=anime.animeName)
        self.add(anime=anime)
