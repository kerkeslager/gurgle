from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Wish(Base):
    __tablename__ = 'wishes'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.UnicodeText, nullable=False, unique=True)
    priority = sa.Column(sa.Integer, nullable=False, default=0)

metadata = Base.metadata
