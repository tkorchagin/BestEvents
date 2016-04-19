import datetime
from sqlalchemy.dialects.postgresql import ARRAY

__author__ = 'tkorchagin'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger, SmallInteger, Boolean

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DeclBase = declarative_base()


class Category(DeclBase):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    source = Column(String, default='ponominalu')

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Event(DeclBase):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    source = Column(String, default='ponominalu')
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Subevent(DeclBase):
    __tablename__ = "Subevents"

    id = Column(Integer, primary_key=True)
    age = Column(Integer, default=0)
    description = Column(String)
    eticket_only = Column(Boolean, default=False)
    eticket_possible = Column(Boolean, default=False)
    image = Column(String)
    link = Column(String)
    sectors_list = Column(ARRAY(Integer))
    subevent_date = Column(DateTime)
    subevent_type = Column(DateTime)
    title = Column(DateTime)
    source = Column(String, default='ponominalu')

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Venue(DeclBase):
    __tablename__ = "Venues"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    description = Column(String)
    eng_title = Column(String)
    google_address = Column(String)
    title = Column(String)
    type = Column(Integer)
    region_id = Column(Integer)
    image_global = Column(String)
    source = Column(String, default='ponominalu')

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Ticket(DeclBase):
    __tablename__ = "Tickets"

    id = Column(Integer, primary_key=True)

    number = Column(Integer)
    price = Column(Float)
    row = Column(Integer)
    sector_id = Column(Integer)
    sector_title = Column(String)
    status = Column(Integer)
    source = Column(String, default='ponominalu')

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


if __name__ == '__main__':
    from constants import DB_PATH

    engine = create_engine(DB_PATH)
    SessionClass = sessionmaker(bind=engine)
    DBSession = SessionClass()

    text_event = Event(title='test title', link='http://tkorchagin.me/')
    DBSession.add_all([text_event])
    DBSession.flush()
    DBSession.commit()
