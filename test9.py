from bs4 import BeautifulSoup
from pprint import pprint
from cfscrape import create_scraper
import mechanicalsoup
from Utils.IO import remove_multiple_spaces
from Utils.Download import download
import re
from os import mkdir, walk, path, rmdir
import zipfile

main_url = 'http://readcomiconline.to'
search_url = main_url + '/AdvanceSearch'
requests = create_scraper()
requests = mechanicalsoup.Browser(requests)


def fill_form(url, data):
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text, 'html.parser')
    form = soup.find('form', attrs={'id': 'formAdvanceSearch'})
    for id, value in data.items():
        form.find(attrs={'id': id})['value'] = value
    return requests.submit(form, web_page.url)


def main(keyword):
    response = fill_form(search_url, {'comicName': keyword})
    web_page = BeautifulSoup(response.text, 'html.parser')
    search_results = web_page.find('table').find_all('td')
    search_results = [BeautifulSoup(search_result['title'])
                      for search_result in search_results
                      if search_result.has_attr('title')]
    new_search_results = []
    for search_result in search_results:
        new_search_results.append({
            'image_url': search_result.find('img')['src'],
            'comic_url': main_url + search_result.find('a')['href'],
            'name': search_result.find('a').text,
            'description': remove_multiple_spaces(search_result.find('p').text)
        })
    return new_search_results


def get_all_images(link):
    response = requests.get(link)
    response = BeautifulSoup(response.text)
    file_name = response.find('title').text.split('-')[0]
    scripts = response.find(attrs={'id': 'containerRoot'}).find_all('script')
    for script in scripts:
        text = re.sub('\s+\s+', '\n', script.text)
        links = re.findall(r'lstImages.push\("(\S+)"\);', text)
        if len(links) > 0:
            i = 0
            try:
                mkdir(file_name)
            except OSError:
                pass
            for link in links:
                download(file_name + '/' + str(i) + '.jpg', link)
                i += 1
            zip_it(file_name + '.cbz', file_name)
            return links


def zip_it(file_name, folder_name):
    zip_file = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in walk(folder_name + '/'):
        for f in files:
            zip_file.write(path.join(root, f))
    zip_file.close()


if __name__ == '__main__':
    zip_it('test9.cbz', 'test')
    # pprint(get_all_images('http://readcomiconline.to/Comic/Batman-Beyond-Rebirth/Full?id=90709&readType=1'))
