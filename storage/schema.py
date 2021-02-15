from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.UnicodeText, nullable=False, unique=True)
    title = sa.Column(sa.Unicode(256), nullable=True)

class Link(Base):
    __tablename__ = 'links'

    id = sa.Column(sa.Integer, primary_key=True)
    source = sa.Column(
        sa.Integer,
        sa.ForeignKey('pages.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    destination = sa.Column(sa.UnicodeText, nullable=False)

class Wish(Base):
    __tablename__ = 'wishes'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.UnicodeText, nullable=False, unique=True)
    priority = sa.Column(sa.Integer, nullable=False, default=0)

metadata = Base.metadata
