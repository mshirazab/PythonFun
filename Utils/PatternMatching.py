import re


class PatternMatching(object):
    def __init__(self, pattern):
        self.__pattern = re.compile(pattern)

    def __call__(self, driver):
        response = driver.page_source
        if len(re.findall(self.__pattern, response)) == 0:
            return False
        else:
            return True
