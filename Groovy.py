"""
This a groove for python
"""
import eyed3
import requests
from json import loads
from os import listdir, remove

groove_search_link = 'https://music.xboxlive.com/1/content/music/search'
access_token_link = 'https://login.live.com/accesstoken.srf'
access_token = 'EgBrAQMAAAAEgAAADAABukHoyu4JEdJSI+OCNNA8j1fjuvZMPyMj7kAJroW8MVT8MKvwfZSLRtB5qBZGrublOLkSr7Z+I4mEX+tgFsUj5c2bctddZ8YE2SgtAKPIShAHDBKdxkReSvhiYq0WJ4Q/Ahxk9ihKGaWfzGCEXMfmY7nM7uSK4ufBlEtCTkYAM2Hkpr/hNSVML7GJhaHNjcYVg3yVShXyDksSlMpoEgVpXPMdUf4ymobdBH7zOMsIuVc73HD81ALgjEdZeOJD/DLPghf/LNccm3bJbDKwDgn/1MY7dWrIJLfs5WidV2EL3lIhcju4V4/MD//B4USghIRe3JMLYjjrBq9q7/EzHm3iAVoAWgBaAAAAAAAfNx5IqfZFWan2RVmIgQQADQAxMzcuOTcuOC4yNDYAAAAAAC0AYXBwaWQ6Ly8xOWNkYzI3Mi04ZWZiLTQ0MGQtOGY4Yi0yMTExOThhMTg3NzUA'


def main():
    keyword = raw_input('Enter song to be searched for: ')
    response = search(keyword)
    for item in response:
        print item['Name'], '|',
        print item['Album'], '|',
        print item['Artists']
        print item['Albumart']
        print
    keyword = input('Enter the index: ')
    keyword -= 1
    filename = 'Ed Sheeran - Castle on the Hill.mp3'
    audio_file = eyed3.load(filename)
    print 'Before changing'
    print audio_file.tag.artist
    print audio_file.tag.album
    print audio_file.tag.title
    print audio_file.tag.track_num

    audio_file.tag.artist = response[keyword]['Artists']
    audio_file.tag.album = response[keyword]['Album']
    audio_file.tag.title = response[keyword]['Name']
    audio_file.tag.track_num = (1, None)
    audio_file.tag.save()
    audio_file = eyed3.load(filename)
    print 'after'
    print audio_file.tag.artist
    print audio_file.tag.album
    print audio_file.tag.title
    print audio_file.tag.track_num


def groom(string):
    string = string.split('Ft')[0]
    string = string.split('&')[0]
    string = string.split('/')[0]
    return string


def test():
    folder_name = 'Music'
    music_files = [item for item in listdir(folder_name)
                   if item.split('.')[-1] == 'mp3']
    for music_file in music_files:
        filename = folder_name + '/' + music_file
        audio_file = eyed3.load(filename)
        print music_file
        print audio_file.tag.artist, '|',
        print audio_file.tag.album, '|',
        print audio_file.tag.title
        print
        keyword = '.'.join(music_file.split('.')[:-1])
        try:
            response = search(keyword)
        except KeyError:
            response = raw_input('Enter a keyword :')
            response = search(response)
        for item in response:
            print item['Name'], '|',
            print item['Album'], '|',
            print item['Artists']
            print item['Albumart']
        keyword = input('Enter the index: ')
        if keyword == -1:
            continue
        elif keyword == 0:
            response = raw_input('Enter a keyword :')
            response = search(response)
            for item in response:
                print item['Name'], '|',
                print item['Album'], '|',
                print item['Artists']
                print item['Albumart']
            keyword = input('Enter the index: ')
            if keyword == -1:
                continue
        keyword -= 1
        audio_file.tag.clear()
        audio_file.tag.artist = response[keyword]['Artists']
        audio_file.tag.album = response[keyword]['Album']
        audio_file.tag.title = response[keyword]['Name']
        audio_file.tag.genre = response[keyword]['Genres']
        audio_file.tag.track_num = (1, None)
        r = requests.get(response[keyword]['Albumart'], stream=True)
        if r.status_code == 200:
            with open('temp.jpg', 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        with open('temp.jpg', 'rb') as f:
            audio_file.tag.images.set(3, f.read(), "image/jpg",
                                      response[keyword]['Artists'] + ' - ' + response[keyword]['Album'])
        remove('temp.jpg')
        audio_file.tag.save(filename)


def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.live.com',
        'Content-Length': '123'
    }
    data = 'grant_type=client_credentials'
    data += '&client_id=19cdc272-8efb-440d-8f8b-211198a18775'
    data += '&client_secret=Eqh74hicApRHhPMGcpiY3Xh'
    data += '&scope=app.music.xboxlive.com'
    print data
    response = requests.post(access_token_link, data=data, headers=headers)
    print response.text


def search(keyword):
    params = {
        'q': keyword,
        'maxItems': 5,
        'filters': 'tracks'
    }
    headers = {
        'Accept': 'application / json',
        'Authorization': 'Bearer ' + access_token,
        'Host': 'music.xboxlive.com'
    }
    response = requests.get(groove_search_link, params=params, headers=headers)
    print response.text
    json_data = loads(response.text)['Tracks']['Items']
    data_needed = []
    for item in json_data:
        new_item = {
            'Name': item['Name'],
            'Album': item['Album']['Name'],
            'Albumart': item['Album']['ImageUrl'],
            'Genres': ', '.join(item['Genres']),
            'Explicit': item['IsExplicit'],
            'Artists': [i['Artist']['Name'] for i in item['Artists']]
            # 'Artists': ', '.join([i['Artist']['Name'] for i in item['Artists']])
        }
        data_needed.append(new_item)
    return data_needed


if __name__ == '__main__':
    test()
