from json import dump, load

import requests as req
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.common.exceptions import *
from time import sleep
from Utils import IO


class Anime(object):
    __main_url = 'http://horriblesubs.info'
    __search_url = __main_url + '/shows/'
    __file_name = 'anime.json'

    @staticmethod
    def search(keyword):
        keyword = keyword.lower()
        try:
            response = req.get(Anime.__search_url).text
        except ConnectionError:
            print IO.Message.error, 'No internet connection'
            return
        response = BeautifulSoup(response, 'html.parser')
        response = {Anime.__main_url + item['href']: item.text for item in response.find_all('a') if
                    keyword in item.text.lower()}
        print IO.Message.searched, keyword
        return response

    @staticmethod
    def add_anime(link):
        try:
            with open(Anime.__file_name, 'r') as fp:
                data = load(fp)
                if data.get('links') is None:
                    data['links'] = {}
        except IOError:
            data = {'links': {}}
        if data['links'].get(link) is not None:
            print IO.Message.error, 'Already added'
            return
        try:
            response = BeautifulSoup(req.get(link).text)
        except ConnectionError:
            print IO.Message.error, 'No internet connection'
            return
        name = response.find(attrs={'class': 'entry-title'}).text
        data['links'][link] = name
        with open(Anime.__file_name, 'w') as fp:
            dump(data, fp)
            print IO.Message.added, name
        Anime.update_episodes(link)

    @staticmethod
    def update_episodes(link):
        driver = webdriver.PhantomJS()
        driver.get(link)
        try:
            while True:
                driver.find_element_by_class_name('morebutton').click()
                sleep(4)
        except NoSuchElementException:
            pass
        except NoSuchWindowException:
            driver.save_screenshot('error.png')
        response = driver.page_source
        response = BeautifulSoup(response, 'html.parser')
        if response.find('div') is None:
            print IO.Message.error, 'No internet connection'
            raise ConnectionError
        anime_name = response.find(attrs={'class': 'entry-title'}).text
        response = response.find(attrs={'class': 'hs-shows'})
        items = response.find_all('td')
        try:
            with open(Anime.__file_name, 'r') as fp:
                organiser = load(fp)['anime']
        except IOError:
            organiser = {}
        organiser[anime_name] = []
        current_episode = None
        clarity = ''
        for item in items:
            if 'rls-label' in item['class']:
                try:
                    if current_episode is not None:
                        organiser[anime_name].insert(0, current_episode_data)
                    current_episode = item.text.split(' ')[-1]
                except ValueError:
                    current_episode = None
                date = item.text.split(' ')[0]
                current_episode_data = {'episode_number': current_episode, 'date': date}
            elif 'dl-label' in item['class']:
                clarity = item.text.split(' ')[-1]
                current_episode_data[clarity] = {}
            elif 'dl-type' in item['class']:
                link = item.find('a')
                if link is not None and link.text == 'Magnet':
                    current_episode_data[clarity] = link['href']
        if current_episode is not None:
            organiser[anime_name].insert(0, current_episode_data)
        with open(Anime.__file_name, 'r') as fp:
            data = load(fp)
            data['anime'][anime_name] = sorted(organiser[anime_name], key=lambda k: k['episode_number'])
        # data['anime'][anime_name] = Anime.__json_sort(organiser[anime_name])
        with open(Anime.__file_name, 'w') as fp:
            dump(data, fp)
        print IO.Message.updated, anime_name

    @staticmethod
    def update_all_episodes():
        with open(Anime.__file_name, 'r') as fp:
            data = load(fp)
        links = data['links'].keys()
        for link in links:
            Anime.update_episodes(link)

    @staticmethod
    def use_page_source():
        with open(Anime.__file_name, 'r') as fp:
            organiser = load(fp)['anime']
        return organiser
