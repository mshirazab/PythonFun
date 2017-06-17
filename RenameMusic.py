import eyed3
import requests
from json import loads
from os import listdir, remove, rename
import warnings

warnings.filterwarnings('ignore')


def main():
    folder_name = 'hello'
    music_files = [item for item in listdir(folder_name)
                   if item.split('.')[-1] == 'mp3']
    for music_file in music_files:
        filename = folder_name + '/' + music_file
        audio_file = eyed3.load(filename)
        print audio_file.tag.artist, '|',
        print audio_file.tag.album, '|',
        print audio_file.tag.title
        new_filename = folder_name + '/' + audio_file.tag.artist + ' - ' + audio_file.tag.title + '.mp3'
        print 'mv "', filename, '" "', new_filename, '"'
        rename(filename, new_filename)

if __name__ == '__main__':
    main()
