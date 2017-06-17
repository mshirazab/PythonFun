from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import requests
from pprint import pprint
import re
import json
from os import remove
from time import time, sleep
from urllib import urlencode
from requests.exceptions import ConnectionError

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

mainURL = 'https://9anime.to'


def main():
    # driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1120, 550)
    link = 'https://9anime.to/watch/shingeki-no-kyojin-season-2.3v16'
    # driver.get(link)
    # driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    # response = driver.page_source
    # driver.quit()
    print 'Getting all episode links'
    response = requests.get(link).text
    response = BeautifulSoup(response, 'html.parser')
    servers = response.find_all('div', attrs={'class': 'server row'})
    server = servers[0]
    attrs = {
        'data-id': re.compile(r'\S+'),
        'data-title': re.compile(r'\S+')
    }
    server_episodes = server.find_all('a', attrs=attrs)
    episode_links = [server_episode['data-id']
                     for server_episode in server_episodes]
    episode_links = [link + '/' + episode_link for episode_link in episode_links]
    responses = []
    print 'Getting video link'
    for link in episode_links[:1]:
        driver.get(link)
        # WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jw-video')))
        # responses.append(driver.page_source)
        sleep(10)
        response = driver.page_source
        response = BeautifulSoup(response, 'html.parser')
        pprint(response.find_all('video'))
        pprint(response.find_all('iframe'))
    driver.quit()


def get_page():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1120, 550)
    link = 'https://9anime.to/watch/shingeki-no-kyojin-season-2.3v16'
    print 'Getting all episode links'
    response = requests.get(link).text
    response = BeautifulSoup(response, 'html.parser')
    servers = response.find_all('div', attrs={'class': 'server row'})
    server = servers[0]
    attrs = {
        'data-id': re.compile(r'\S+'),
        'data-title': re.compile(r'\S+')
    }
    server_episodes = server.find_all('a', attrs=attrs)
    episode_links = [server_episode['data-id']
                     for server_episode in server_episodes]
    episode_links = [link + '/' + episode_link for episode_link in episode_links]
    responses = []
    print 'Getting video link'
    with open('episode.html', 'w') as fp:
        for episode_link in episode_links[:1]:
            driver.get(link)
            # WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jw-video')))
            # responses.append(driver.page_source)
            sleep(10)
            response = driver.page_source
            fp.write(response.encode('utf-8'))


def use_page():
    try:
        with open('episode.html', 'r') as fp:
            response = BeautifulSoup(fp, 'html.parser')
    except IOError:
        print '[ ERROR ]File not found'
        return
    video = response.find(attrs={'id': 'player'})

    video = video.find(attrs={'allowfullscreen': re.compile(r'\S+')})
    video_link = 'https:' + video['src']
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1120, 550)
    driver.get(video_link)
    sleep(5)
    response = BeautifulSoup(driver.page_source, 'html.parser')
    pprint(response.find_all('video'))


if __name__ == '__main__':
    link = 'https://9anime.to/watch/shingeki-no-kyojin-season-2.3v16'
    response = requests.get(link).text
    response = BeautifulSoup(response, 'html.parser')
    video_player = response.find(attrs={'id': 'player'})
    print video_player
    print video_player.find_all('iframe')

    '''
    
    
    class Anime:
        def __init__(self):
            self.json_filename = '.anime.json'
            self.main_url = 'https://9anime.to'
            self.search_url = self.main_url + '/search'
    
        def __add_anime(self, anime_name, anime_url):
            json_data = {'anime': []}
            try:
                with open(self.json_filename, 'r') as fp:
                    json_data = json.load(fp)
            except IOError:
                pass
            json_data['anime'].append({
                'name': anime_name,
                'url': anime_url
            })
            with open(self.json_filename, 'w') as fp:
                json.dump(json_data, fp)
    
        def remove_anime(self):
            try:
                with open(self.json_filename, 'r') as fp1:
                    animes = json.load(fp1)['anime']
                    for i in range(len(animes)):
                        print i + 1, '|', animes[i]['name']
                    choice = input('Which one do you want to remove: ')
                    choice -= 1
                    if 0 <= choice < len(animes):
                        del animes[choice]
                        with open(self.json_filename, 'w') as fp2:
                            json.dump({'anime': animes}, fp2)
            except IOError:
                pass
    
        def get_anime_episodes(self):
            try:
                with open(self.json_filename, 'r+') as fp:
                    animes = json.load(fp)['anime']
                    anime_names = [anime['name'] for anime in animes]
                    anime_urls = [anime['url'] for anime in animes]
                    anime_dates = [anime.get('date') for anime in animes]
                    for i in range(len(anime_names)):
                        print i + 1, '|', anime_names[i]
                    position = input('Which anime list do you want: ')
                    position -= 1
                    if 0 <= position < len(anime_names):
                        anime_date = anime_dates[position]
                        if anime_date is None or anime_date < time():
                            response = requests.get(anime_urls[position]).text
                            response = BeautifulSoup(response, 'html.parser')
                            servers = response.find_all('div', attrs={'class': 'server row'})
                            anime_date = self.__get_time(response)
                            server = servers[0]
                            attrs = {
                                'data-id': re.compile(r'\S+'),
                                'data-title': re.compile(r'\S+')
                            }
                            server_episodes = server.find_all('a', attrs=attrs)
                            episode_links = [server_episode['data-id']
                                             for server_episode in server_episodes]
                            pprint(episode_links)
                            animes[position] = {
                                'name': anime_names[position],
                                'url': anime_urls[position],
                                'date': anime_date,
                                'links': episode_links
                            }
                            fp.seek(0)
                            fp.truncate()
                            json.dump({'anime': animes}, fp)
                        else:
                            pprint([animes[position]['url'] + '/' + link for link in animes[position]['links']])
            except IOError:
                print 'Error: Anime not found in the json file\n\t\tMake sure you add it in the json file'
    
        def search_anime(self, keyword):
            response = requests.get(self.search_url, params={'keyword': keyword}).text
            response = BeautifulSoup(response, 'html.parser')
            search_results = response.find_all('div', attrs={'class': re.compile(r'item')})
            search_results = [search_result.find_all('a')[-1] for search_result in search_results]
            search_results = [{'url': search_result['href'], 'name': search_result.text}
                              for search_result in search_results]
            for i in range(len(search_results)):
                print i + 1, '|', search_results[i]['name']
            choice = input('Do you want to add any anime into your collection: ')
            choice -= 1
            if 0 <= choice < len(search_results):
                anime_name = search_results[choice]['name']
                anime_url = search_results[choice]['url']
                self.__add_anime(anime_name, anime_url)
    
        @staticmethod
        def __get_time(response):
            if len(response.find_all(class_='alert alert-primary')) == 2:
                episode_time = response.find_all(class_='alert alert-primary')[-1].find('i').text
                days, temp, hours, temp, minutes, temp = episode_time.split(' ')
                print days, hours, minutes
                return int(days) * 24 * 60 * 60 + \
                       int(hours) * 60 * 60 + \
                       int(minutes) * 60 + time()
            else:
                return time() * 5
    
        def updates(self):
            with open(self.json_filename, 'r+') as fp:
                animes = json.load(fp)['anime']
                for anime in animes:
                    anime_name = anime['name']
                    anime_date = anime['date']
                    print anime_name, '\t', '|',
                    if anime_date is None:
                        print 'Please run get_episodes() before this'
                    elif anime_date > time():
                        seconds_left = anime_date - time()
                        days_left = int(seconds_left / (60 * 60 * 24))
                        if days_left > 200:
                            print 'Completed'
                            continue
                        seconds_left %= 60 * 60 * 24
                        hours_left = int(seconds_left / 3600)
                        seconds_left %= 60 * 60
                        minutes_left = int(seconds_left / 60)
                        print 'No updates until', days_left, 'days', hours_left, 'hours', minutes_left, 'minutes'
                    else:
                        response = requests.get(anime['url']).text
                        response = BeautifulSoup(response, 'html.parser')
                        servers = response.find_all('div', attrs={'class': 'server row'})
                        server = servers[0]
                        attrs = {
                            'data-id': re.compile(r'\S+'),
                            'data-title': re.compile(r'\S+')
                        }
                        server_episode = server.find_all('a', attrs=attrs)[-1]
                        episode_link = self.main_url + server_episode['href']
                        print episode_link
    
    
    def main():
        ani = Anime()
        while True:
            prompt = 'MENU\n1.Search anime\n2.Delete anime \n3.Get episodes\n4.Updates\n5.Exit\nEnter choice: '
            choice = input(prompt)
            try:
                if choice == 1:
                    search = raw_input('Enter keyword to search: ')
                    ani.search_anime(search)
                elif choice == 2:
                    ani.remove_anime()
                elif choice == 3:
                    ani.get_anime_episodes()
                elif choice == 4:
                    ani.updates()
                elif choice == 5:
                    exit(0)
                else:
                    print 'wrong choice'
            except ConnectionError:
                print 'There is no internet connection'
    
    
    if __name__ == '__main__':
        main()
    '''
