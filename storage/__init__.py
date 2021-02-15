import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from . import schema

class Store(object):
    def __init__(self):
        self.engine = sa.create_engine('sqlite:///db.sqlite3')

    def queue_wish(self, url):
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

            session.commit()

        return url

    def dequeue_wish(self, url):
        with sa_orm.Session(self.engine) as session:
            session.execute(sa.delete(schema.Wish).filter_by(url=url))
            session.commit()

    def update_moved_link(self, old, new):
        with sa_orm.Session(self.engine) as session:
            if session.query(schema.Wish).filter_by(url=new).count() == 0:
                session.query(schema.Wish).filter_by(url=old).update({'url': new })
            else:
                old_wish = session.query(schema.Wish).filter_by(url=old).scalar()
                new_wish = session.query(schema.Wish).filter_by(url=new).scalar()
                session.query(schema.Wish).filter_by(url=new).update({'priority': old_wish.priority + new_wish.priority })
                session.query(schema.Wish).filter_by(url=old).delete()
            session.commit()

    def create_page(self, url, title):
        with sa_orm.Session(self.engine) as session:
            session.execute(sa.delete(schema.Page).filter_by(url=url))

            page = schema.Page(url=url, title=title)
            session.add(page)
            session.commit()
            return page.id

    def create_link(self, source_page_id, destination_url):
        with sa_orm.Session(self.engine) as session:
            link = schema.Link(source=source_page_id, destination=destination_url)
            session.add(link)
            session.commit()
