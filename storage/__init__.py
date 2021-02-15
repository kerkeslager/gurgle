import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from . import schema

class Store(object):
    def __init__(self):
        self.engine = sa.create_engine('sqlite:///db.sqlite3')

    def add_wish(self, url):
        with sa_orm.Session(self.engine) as session:
            wishes_for_url = session.query(schema.Wish).filter_by(url=url)

            if wishes_for_url.count() == 0:
                wish = schema.Wish(url=url)
                session.add(wish)

            else:
                wish = wishes_for_url.scalar()
                wish.priority = wish.priority + 1
                session.add(wish)

            session.commit()

    def get_next_wish(self):
        with sa_orm.Session(self.engine) as session:
            wish = session.execute(sa.select(schema.Wish).order_by(sa.desc('priority'), 'id')).scalar()

            if wish is None:
                return None

            url = wish.url
            session.delete(wish)
            session.commit()

        return url

