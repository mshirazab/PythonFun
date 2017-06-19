from mechanicalsoup import Browser, Form
from cfscrape import create_scraper
import re


def search(url, keyword, cloudflare_needed=False):
    if cloudflare_needed:
        requests = create_scraper()
        requests = Browser(requests)
    else:
        requests = Browser()
    web_page = requests.get(url)
    forms = web_page.soup.find_all('form')
    search_text = re.compile(r'[\s\S]*[Ss]earch[\s\S]*')
    forms = [form for form in forms if bool(re.search(search_text, str(form)))]
    form = forms[0]
    search_input = form.find('input', attrs={'type': 'text'})
    if search_input is None:
        search_input = form.find('input', attrs={'type': 'search'})
    search_input['value'] = keyword
    for inp in form.find_all(attrs={'type': 'submit'}):
        if bool(re.search(search_text, str(inp))):
            inp['name'] = 'Search'
        else:
            inp['name'] = ''
    if url in form.attrs['action']:
        url = form.attrs['action']
    else:
        url = url + form.attrs['action']
    form = Form(form)
    form.choose_submit('Search')
    return requests.submit(form, url).text


if __name__ == '__main__':
    print search('https://ww1.gogoanime.io', 'boku', True)
