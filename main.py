import sqlalchemy as sa

import storage

store = storage.Store()
store.add_wish('https://en.wikipedia.org/')
print([w.url for w in store.get_wishes()])
