from Anime import Anime
from bs4 import BeautifulSoup
import urllib2
from EpisodeUnit import EpisodeUnit


class Episode(object):
    def __init__(self, anime):
        self.__anime = anime
        self.__episodes = []
        self.__seasons = 0
        self.__getEpisodes()

    def __getEpisodes(self):
        print "Scraping Wikipedia for episode list of "+self.__anime.animeName
        for wikiUrl in self.__anime.wikiUrls:
            response = urllib2.urlopen(wikiUrl)
            soup = BeautifulSoup(response, 'html5lib')
            tables = soup.find_all('table', class_='wikitable')
            seasons = soup.find_all('span', class_='mw-headline')
            relativeEpisodeNumber = 0
            for i in range(len(tables)):
                episodes = tables[i].find_all('tr', class_='vevent')
                season = seasons[i + 1].string
                if 'Season' in season or 'season' in season:
                    self.__seasons += 1
                    if len(self.__anime.gogoUrls) != 1:
                        relativeEpisodeNumber = 0
                    for episode in episodes:
                        try:
                            episodeNumber = int(episode.find('th').string)
                            relativeEpisodeNumber += 1
                            episodeName = str(episode.find('td', class_='summary'))
                            episodeName = episodeName.split('"')[5]
                            episodeDate = str(episode.find_all('td')[-2])
                            episodeDate = episodeDate.split('>')[1].split('<')[0]
                            if (str(episode.find('td', class_='summary')) ==
                                    str(episode.find_all('td')[-2])):
                                episodeDate = str(episode.find_all('td')[-1])
                                episodeDate = episodeDate.split('>')[1].split('<')[0]
                            episode = EpisodeUnit(episodeName, episodeNumber, episodeDate,
                                                  url=self.__getURL(seasonNumber=self.__seasons,
                                                                    episodeNumber=relativeEpisodeNumber))
                            self.__episodes.append(episode.getDictionary())
                        except ValueError:
                            pass
        print "DONE"

    def __getURL(self, seasonNumber, episodeNumber):
        if len(self.__anime.gogoUrls) == 1:
            return self.__anime.gogoUrls[0] + '-' + str(episodeNumber)
        else:
            return self.__anime.gogoUrls[seasonNumber - 1] + '-' + str(episodeNumber)

    def getEpisodeDictionary(self):
        A = {'Name': self.__anime.animeName,
             'Seasons': self.__seasons,
             'Episodes': self.__episodes}
        return A
