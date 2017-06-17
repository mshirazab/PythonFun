from pprint import pprint
import cfscrape
from urllib import urlencode
from bs4 import BeautifulSoup
import re
import sys
import os

requests = cfscrape.create_scraper()
main_url = 'https://ww1.gogoanime.io/'
search_url = main_url + 'search.html?'
description_url = main_url + '/category/'
image_url = 'https://images.gogoanime.tv/cover/'  # add png in the end


def search():
    query = {
        'keyword': 'boku no hero'
    }
    link = search_url + urlencode(query)
    response = requests.get(link).text
    response = BeautifulSoup(response, 'html.parser')
    results = response.find(attrs={'class': 'items'})
    results = results.find_all('a')
    new_results = []
    for i in range(0, len(results), 2):
        new_results.append({
            'name': results[i]['title'],
            'link': results[i]['href'].split('/')[-1],
            'image': results[i].find('img')['src']
        })
    # pprint(new_results)
    result_link = description_url + new_results[0]['link']
    response = requests.get(result_link).text
    response = BeautifulSoup(response, 'html.parser')
    episode_list = response.find(attrs={'class': 'anime_video_body'})
    episode_number = episode_list.find_all('a')[-1]['ep_end']


def download():
    url = 'https://r8---sn-gwpa-jv3z.googlevideo.com/videoplayback?id=4af542f051c26247&itag=18&source=webdrive&requiressl=yes&ttl=transient&pl=36&ei=1Xc6WeHRLo7_qQXCkahg&driveid=0ByH-OssUbuomZDVRVmQ1d3Z2dnc&mime=video/mp4&lmt=1496905670549029&ip=2a02:5060:501:c049::3&ipbits=0&expire=1497018389&sparams=driveid,ei,expire,id,ip,ipbits,itag,lmt,mime,mip,mm,mn,ms,mv,pl,requiressl,source,ttl&signature=72F983776B58F79B8A4A13DCBC4AE3030770ED28.53320FA50007F48066410B92092EDBB53C59E319&key=cms1&app=explorer&cms_redirect=yes&mip=2405:204:d009:1a4:4804:f35e:f98d:a997&mm=31&mn=sn-gwpa-jv3z&ms=au&mt=1497004475&mv=m'
    fileName = 'videoplayback.mp4'
    if fileName in os.listdir(os.getcwd()):
        return
    response = requests.get(url, stream=True)
    print "Downloading " + fileName
    try:
        with open(fileName, 'wb') as file:
            i = 1
            for chunk in response.iter_content(chunk_size=1):
                print "\rDownloaded " + str(i) + " bytes",
                sys.stdout.flush()
                file.write(chunk)
                i += 1
        print "\nDOWNLOAD COMPLETE\n"
    except KeyboardInterrupt:
        print
        print "\rDOWNLOAD INTERRUPTED"
        os.remove(fileName)
        exit(1)

if __name__ == '__main__':
    download()
