import requests
import sys
import os


def download(file_name, url):
    response = requests.get(url, stream=True)
    print "Downloading " + file_name
    try:
        with open(file_name, 'wb') as file:
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
        os.remove(file_name)
        exit(1)
