from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
from pprint import pprint
import json

search_button_id = 'btnSubmit'
search_bar_id = 'animeName'
main_url = 'http://kissanime.ru'
search_url = main_url + '/AdvanceSearch'
json_filename = '.kissanime.json'
anime_name_id = 'name'
anime_link_id = 'link'


def search(keyword):
    driver = webdriver.Chrome('./chromedriver')
    link = search_url
    try:
        driver.get(link)
        method = PatternMatching(r'bubbles')
        WebDriverWait(driver, 50).until_not(method)
        driver.find_element_by_id(search_bar_id).send_keys(keyword)
        driver.find_element_by_id(search_button_id).click()
        response = driver.page_source
    except NoSuchElementException:
        driver.save_screenshot('screenshot.png')
        return
    response = BeautifulSoup(response, 'html.parser')
    table = response.find(attrs={'class': 'listing'})
    results = table.find_all('a')
    results = [{
        'name': str(result.text).lstrip(),
        'link': main_url + result['href']
    } for result in results]
    return results


class PatternMatching(object):
    def __init__(self, pattern):
        self.__pattern = re.compile(pattern)

    def __call__(self, driver):
        response = driver.page_source
        if len(re.findall(self.__pattern, response)) == 0:
            return False
        else:
            return True


def use_saved():
    with open('test6.html', 'r') as fp:
        response = fp.read()
    response = BeautifulSoup(response, 'html.parser')
    table = response.find(attrs={'class': 'listing'})
    results = table.find_all('a')
    results = [{
        'name': str(result.text).lstrip(),
        'link': main_url + result['href']
    } for result in results]
    pprint(results)


if __name__ == '__main__':
    results = search('boruto')
    length = len(results)
    pprint([str(i + 1) + ' | ' + results[i]['name'] for i in range(length)])
    choice = input('Do you want to add anything to your collection: ')
    choice -= 1
    if 0 <= choice < length:
        choice = results[choice]
        json_data = {'anime': []}
        try:
            with open(json_filename, 'r') as fp:
                json_data = json.load(fp)
        except IOError:
            pass
        json_data['anime'].append({
            'name': choice['name'],
            'link': choice['link']
        })
        with open(json_filename, 'w') as fp:
            json.dump(json_data, fp)
