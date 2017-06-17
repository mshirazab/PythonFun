import requests
import re
from pprint import pprint
search_header = "https://www.google.co.in/search?q="
link_header = "https://www.google.co.in/url?q="

def main():
    response = requests.get("https://www.google.co.in/search?q=myanimelist")
    links = re.compile(r'href="/url\?q=(\S+)"').findall(response.text)
    links = [link.split('&')[0] for link in links]
    response = requests.get(links[0])
    print response.text


if __name__ == '__main__':
    main()
