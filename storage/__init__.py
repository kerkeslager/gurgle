import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from . import schema

class Store(object):
    def __init__(self):
        self.engine = sa.create_engine('sqlite:///db.sqlite3')

    def add_wish(self, url):
        with sa_orm.Session(self.engine) as session:
            wish = schema.Wish(url=url)
            session.add(wish)
            session.commit()

    def get_wishes(self):
        with sa_orm.Session(self.engine) as session:
            return session.execute(sa.select(schema.Wish).order_by('id')).scalars().all()

