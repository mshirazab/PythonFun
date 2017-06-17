#!/usr/bin/python3
"""Script to notify results."""

import cfscrape
from bs4 import BeautifulSoup
from pprint import pprint
import requests

scraper = cfscrape.create_scraper()
mainURL = 'https://ww1.gogoanime.io/'
wikiURL = 'https://en.wikipedia.org/w/index.php'


def search(keyword):
    link = mainURL + '/search.html?keyword=' + keyword.replace(' ', '-')
    response = scraper.get(link).content
    soupedData = BeautifulSoup(response, 'html.parser')
    table1 = soupedData.find(class_='main_body')
    rows = table1.find_all('a')
    animes = []
    for row in rows:
        if row.get('data-page') == None:
            animes.append(row)
    new_animes = []
    for i in range(0, len(animes), 2):
        new_animes.append({
            'link': mainURL + animes[i]['href'],
            'text': animes[i + 1].text
        })
    pprint(new_animes)


def getEpisodes(anime_name):
    link = wikiURL + '?search=List-of-' + anime_name.replace(' ', '-') + '-episodes'
    response = requests.get(link).content
    with open('hello.html', 'w') as fp:
        fp.write(response)
    soupedData = BeautifulSoup(response, 'html.parser')
    tables = soupedData.find_all(class_='wikitable')
    if len(tables) == 0:
        print 'not there yet'
        links = soupedData.find_all('a')
        newlinks = []
        for link in links:
            if link.get('data-serp-pos') != None:
                newlinks.append(link)
        pprint(newlinks)


def download(anime_name, episode_number):
    torrentURL = 'http://1337x.to'
    response = requests.get(
        torrentURL + '/search/' + anime_name.replace(' ', '+') + '+' + episode_number + '/1/').content
    soupedData = BeautifulSoup(response, 'html.parser')
    rows = soupedData.find('tbody').find_all('tr')
    links = [row.find_all('a')[1] for row in rows]
    seeds = [row.find(class_='seeds') for row in rows]
    leeches = [row.find(class_='leeches') for row in rows]
    size = [row.find(class_='size') for row in rows]
    new_links = []
    for i in range(len(links)):
        link = links[i]
        link = link['href']
        if 'torrent' in link and not 'http' in link:
            response = scraper.get(torrentURL + link).content
            soupedData = BeautifulSoup(response, 'html.parser')
            name = soupedData.find(class_='box-info-heading').text
            link = soupedData.find(class_='btn-magnet')['href']
            new_links.append(
                {'name': name, 'link': link, 'seeds': seeds[i].text, 'leeches': leeches[i].text, 'size': size[i].text})
    pprint(new_links)  # getEpisodes('boruto')


download('one piece', '789')
