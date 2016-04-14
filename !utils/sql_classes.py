import datetime
from sqlalchemy.dialects.postgresql import ARRAY

__author__ = 'tkorchagin'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger, SmallInteger, Boolean

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DeclBase = declarative_base()


class Event(DeclBase):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Subevent(DeclBase):
    __tablename__ = "Subevents"

    id = Column(Integer, primary_key=True)
    str_date = Column(String)
    annotation = Column(String)
    link = Column(String)
    subevent_date = Column(DateTime)
    commission = Column(Integer)
    eticket_possible = Column(Boolean, default=False)
    age = Column(Integer, default=0)
    credit_card_payment = Column(Boolean, default=False)
    sectors_list = Column(ARRAY(Integer))
    source = Column(String)
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
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class Ticket(DeclBase):
    __tablename__ = "Tickets"

    id = Column(Integer, primary_key=True)
    sector_id = Column(Integer)
    price = Column(Float)
    seat = Column(Integer)
    row = Column(Integer)
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
