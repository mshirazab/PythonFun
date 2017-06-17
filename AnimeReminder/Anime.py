class Anime(object):
    def __init__(self, animeName, wikiUrls, gogoUrls):
        self.animeName = animeName
        self.wikiUrls = wikiUrls
        self.gogoUrls = gogoUrls

    def getAnimeDictionary(self):
        A = {'Name': self.animeName,
             'WikiURLs': self.wikiUrls,
             'GogoURLs': self.gogoUrls}
        return A
