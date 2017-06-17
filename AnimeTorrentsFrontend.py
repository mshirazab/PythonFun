from flask import Flask, render_template, request, redirect, flash
from AnimeTorrentsBackend import Anime
from requests.exceptions import ConnectionError
import re

app = Flask(__name__)
app.secret_key = 'some_secret'


def episode_list():
    text = HtmlBuilder()
    animes = Anime.use_page_source()
    for anime, episodes in animes.items():
        pattern = re.compile(r'[^a-zA-Z]+')
        anime_no_spaces = pattern.sub('', anime)
        text.open_tag('button', attrs={'type': 'button',
                                       'class': 'anime-btn btn-block btn btn-info',
                                       'data-toggle': 'collapse',
                                       'data-target': '#' + anime_no_spaces,
                                       })
        text.add_data(anime)
        text.close_tag()
        text.open_tag('div', {'id': anime_no_spaces, 'class': 'container-fluid collapse'})
        for i in range(len(episodes)):
            text.open_tag('div', {'class': 'panel row'})
            text.open_tag('div', {'class': 'episode-btn col-xs-3'})
            text.open_tag('p', {'class': 'text-center', 'style': 'margin: 10px;'})
            text.add_data(episodes[i]['episode_number'] + '\t' + episodes[i]['date'])
            text.close_tag()
            text.close_tag()
            clarities = {clarity: link for clarity, link in episodes[i].items()
                         if clarity != 'date' and clarity != 'episode_number'}
            for clarity, link in clarities.items():
                text.open_tag('div', {'class': 'col-xs-3'})
                text.open_tag('a', {'href': link})
                text.open_tag('button', {'type': 'button', 'class': 'btn btn-magnet btn-block'})
                text.add_data(clarity)
                text.close_tag()
                text.close_tag()
                text.close_tag()
            text.close_tag()
        text.close_tag()
    return text.get_html()


has_refreshed = None
searched_keyword = None


@app.route('/')
def main():
    refresh = HtmlBuilder()
    refresh.add_data('<hr>')
    refresh.open_tag('a', {'href': '/refresh'})
    refresh.open_tag('button', {'class': 'btn btn-info btn-block', 'type': 'button'})
    refresh.add_data('Refresh')
    animes = HtmlBuilder()
    animes.add_data('<hr>')
    animes.add_data(episode_list())
    return render_template('sandbox.html',
                           refresh=refresh.get_html(),
                           animes=animes.get_html(),
                           title='Main Page')


@app.route('/refresh')
def refresh():
    try:
        Anime.update_all_episodes()
        flash('Successfully refreshed')
    except ConnectionError:
        flash('No internet connection')
    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        searched_keyword = request.form.values()[0]

        refresh = HtmlBuilder()
        response = Anime.search(searched_keyword)
        refresh.open_tag('div',{'class':'container-fluid'})
        for link, anime in response.items():
            refresh.open_tag('div', {'class': 'panel row'})
            refresh.open_tag('div', {'class': 'col-xs-9'})
            refresh.open_tag('a', {'href': link})
            refresh.add_data(anime)
            refresh.close_tag()
            refresh.close_tag()
            refresh.open_tag('div', {'class': 'col-xs-3'})
            refresh.open_tag('a', {'href': '/add_anime?link=' + link.encode('utf-8')})
            refresh.open_tag('button', {'type': 'button', 'class': 'btn btn-magnet btn-block'})
            refresh.add_data('Add anime')
            refresh.close_tag()
            refresh.close_tag()
            refresh.close_tag()
            refresh.close_tag()
        animes = HtmlBuilder()
        animes.add_data('<hr>')
        animes.add_data(episode_list())
        return render_template('sandbox.html',
                               refresh=refresh.get_html(),
                               animes=animes.get_html(),
                               title='Results for ' + searched_keyword)

    return redirect('/')


@app.route('/add_anime')
def add_anime():
    Anime.add_anime(request.args.get('link'))
    return redirect('/')


class HtmlBuilder(object):
    def __init__(self):
        self.__html = u''
        self.__stack = []

    def __push(self, data):
        self.__stack.append(data)

    def __pop(self):
        return self.__stack.pop()

    def open_tag(self, tag, attrs):
        data = '\n<' + tag  # opening tag
        for right, left in attrs.items():
            data += ' ' + right + '="' + left + '"'
        data += '>'
        self.__push(tag)

        data = ''.join([i if ord(i) < 128 else ' ' for i in data])
        self.__html += data

    def close_tag(self):
        tag = self.__pop()
        self.__html += '</' + tag + '>\n'

    def add_data(self, data):
        self.__html += data

    def get_html(self):
        length = len(self.__stack)
        while length > 0:
            self.close_tag()
            length = len(self.__stack)
        return self.__html
