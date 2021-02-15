import requests
import sqlalchemy as sa

import storage

STARTING_URLS = [
    'https://en.wikipedia.org/',
    'https://fsf.org/',
]

store = storage.Store()

wish = store.get_next_wish()

if wish is None:
    for url in STARTING_URLS:
        store.add_wish(url)

else:
    response = requests.get(wish)
    print(response.text)
