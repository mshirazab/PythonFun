"""
This is a program that tells the amount of internet left in jio XD
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
from pprint import pprint

username_id = 'pt1:r1:0:sb11:it1::content'
button_id = 'pt1:r1:0:sb11:cb1'
password_id = 'pt1:r1:0:sb11:it2::content'
username = 'shiru1234@gmail.com'
password = 'Shiru@1234'
data_id = 'pt1:r1:0:pgl96'


class PatternMatching(object):
    def __init__(self, pattern):
        self.__pattern = re.compile(pattern)

    def __call__(self, driver):
        response = driver.page_source
        if len(re.findall(self.__pattern, response)) == 0:
            return False
        else:
            return True


def main():
    driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    driver.get('https://www.jio.com/Jio/portal/')
    driver.find_element_by_id(username_id).send_keys(username)
    driver.find_element_by_id(password_id).send_keys(password)
    driver.find_element_by_id(button_id).click()
    method = PatternMatching(data_id)
    WebDriverWait(driver, 50).until(method)
    response = BeautifulSoup(driver.page_source, 'html.parser')
    all_left = response.find(attrs={'id': data_id}).find_all(class_='leftValueText')
    pprint([i.text for i in all_left])


if __name__ == '__main__':
    main()
