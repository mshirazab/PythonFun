import datetime
import time


class EpisodeUnit(object):
    def __init__(self, episodeName, episodeNumber, episodeDate, url):
        self.episodeName = episodeName
        self.episodeNumber = episodeNumber
        self.episodeDate = episodeDate
        self.url = url

    def getDictionary(self):
        A = {'Name': self.episodeName,
             'Number': self.episodeNumber,
             'Time': self.episodeDate,
             'URL': self.url}
        return A
