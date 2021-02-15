import cgi
import urllib.parse

import bs4
import requests
import sqlalchemy as sa

import storage

STARTING_URLS = [
    'http://www.aaronsw.com/',
    'https://en.wikipedia.org/',
    'https://fsf.org/',
    'https://www.eff.org/',
    'https://www.gnu.org/',
    'https://www.jwz.org/',
    'https://www.npr.org/',
    'https://www.motherjones.com/',
    'https://www.propublica.org/',
    'https://sci-hub.st/',
]

store = storage.Store()

def is_same_page(url0, url1):
    '''
    Tells if the URLs link to the same page (i.e., detects if one links
    to an anchor on the same page.
    '''
    url0 = urllib.parse.urlparse(url0)
    url1 = urllib.parse.urlparse(url1)

    return url0.scheme == url1.scheme \
        and url0.netloc == url1.netloc \
        and url0.path == url1.path \
        and url0.params == url1.params \
        and url0.query == url1.query

def analyze(response):
    soup = bs4.BeautifulSoup(response.text, features='html.parser')

    title = soup.title.string
    text = soup.get_text()

    page_id = store.create_page(response.url, title)

    for link_node in soup.find_all('a'):
        link_url = link_node.attrs.get('href')

        if link_url is None:
            continue

        absolute_url = urllib.parse.urljoin(response.url, link_url)

        if is_same_page(response.url, absolute_url):
            continue

        store.create_link(page_id, absolute_url)
        store.queue_wish(absolute_url)

        # TODO Analyze link text

    # TODO Analyze the page text

def crawl_once():
    wish = store.get_next_wish()

    if wish is None:
        for url in STARTING_URLS:
            store.queue_wish(url)
        crawl_once()
        return

    print('Emitting HEAD request "{}"'.format(wish))

    response = requests.head(wish)

    if response.status_code == 200:
        # TODO Do cacheing

        content_type = response.headers['Content-Type']
        mime_type, options = cgi.parse_header(content_type)

        if mime_type in ('text/html', 'text/x-web-markdown'):
            response = requests.get(wish)

            # TODO Maybe look at the mime type of the GET, since that's coming back different from the mime type of the HEAD sometimes

            if response.status_code == 200:
                analyze(response)
                store.dequeue_wish(wish)

            else:
                # TODO Handle this situation
                import ipdb; ipdb.set_trace()

        else:
            # TODO Handle other mime types
            import ipdb; ipdb.set_trace()

    elif response.status_code in (301, 302):
        old_location = wish
        new_location = response.headers['Location']

        store.update_moved_link(old_location, new_location)

    else:
        import ipdb; ipdb.set_trace()

crawl_once()
