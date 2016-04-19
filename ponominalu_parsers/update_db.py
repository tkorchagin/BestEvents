import json
import os
import pytz
import sys
sys.path.append('../')
from utils.constants import *
from utils.sql_classes import *

__author__ = 'tkorchagin'

engine = create_engine(DB_PATH)
SessionClass = sessionmaker(bind=engine)
DBSession = SessionClass()


def add_categories(fn, pack_len=500):
    print fn
    categories = []
    cnt = 0

    items = json.load(open(fn))
    for item in items:
        cnt += 1
        if cnt % 100 == 0:
            print 'add_categories %d, %.3f%%' % (cnt, 100 * float(cnt) / len(items))
        category_id = item['category_id']
        title = item['title']

        category = Category(id=category_id, title=title)
        categories.append(category)

        if len(categories) % pack_len == 0:
            DBSession.add_all(categories)
            DBSession.flush()
            DBSession.commit()
            categories = []

    DBSession.add_all(categories)
    DBSession.flush()
    DBSession.commit()


def add_events(fn, pack_len=500):
    print fn
    events = []
    cnt = 0

    events_arr = json.load(open(fn))
    events_len = len(events_arr)
    for el in events_arr:
        cnt += 1
        if cnt % 100 == 0:
            print 'add_events %d, %.3f%%' % (cnt, 100 * float(cnt) / events_len)

        event_id = el['event_id']
        title = el['title']
        description = el['description']

        event = Event(id=event_id, title=title, description=description)
        DBSession.merge(event)
        DBSession.commit()


def add_subevents(fn, pack_len=500):
    print fn
    subevents = []
    cnt = 0
    items = json.load(open(fn))
    for item in items:
        cnt += 1
        if cnt % 100 == 0:
            print 'add_subevents %d, %.3f%%' % (cnt, 100 * float(cnt) / len(items))

        subevent_id = item.get('subevent_id')
        age = item.get('age')
        description = item.get('description')
        eticket_only = item.get('eticket_only')
        eticket_possible = item.get('eticket_possible')
        image = item.get('image')
        link = item.get('link')
        sectors_list = item.get('sectors_ids')

        subevent_date = item.get('subevent_date')
        if subevent_date is None:
            continue
        subevent_date = datetime.datetime.strptime(subevent_date, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.UTC)

        subevent_type = item.get('subevent_type')
        title = item.get('title')

        subevent = Subevent(
            id=subevent_id,
            age=age,
            description=description,
            eticket_only=eticket_only,
            eticket_possible=eticket_possible,
            image=image,
            link=link,
            sectors_list=sectors_list,
            subevent_date=subevent_date,
            subevent_type=subevent_type,
            title=title,
        )
        DBSession.merge(subevent)
        DBSession.commit()


def add_tickets(fn, pack_len=500):
    print fn
    tickets = []
    cnt = 0
    items = json.load(open(fn))
    for item in items:
        cnt += 1
        if cnt % 100 == 0:
            print 'add_tickets %d, %.3f%%' % (cnt, 100 * float(cnt) / len(items))

        ticket_id = item.get('ticket_id')
        number = int(item.get('number'))
        price = item.get('price')
        row = item.get('row')
        sector_id = item.get('sectior_id')
        sector_title = item.get('sector_title')
        status = item.get('status')

        if status != 0:
            continue

        ticket = Ticket(
            id=ticket_id,
            number=number,
            price=price,
            row=row,
            sector_id=sector_id,
            sector_title=sector_title,
            status=status,
        )
        DBSession.merge(ticket)
        DBSession.commit()
    #
    #     tickets.append(ticket)
    #
    #     if len(tickets) % pack_len == 0:
    #         DBSession.add_all(tickets)
    #         DBSession.flush()
    #         DBSession.commit()
    #         tickets = []
    #
    # DBSession.add_all(tickets)
    # DBSession.flush()
    # DBSession.commit()


def add_venues(fn, pack_len=500):
    print fn
    venues = []
    cnt = 0
    items = json.load(open(fn))
    for item in items:
        cnt += 1
        if cnt % 100 == 0:
            print 'add_venues %d, %.3f%%' % (cnt, 100 * float(cnt) / len(items))

        venue_id = item.get('venue_id')
        address = item.get('address')
        title = item.get('title')
        type_id = item.get('type_id')
        region_id = item.get('region_id')

        venue = Venue(
            id=venue_id,
            address=address,
            title=title,
            type_id=type_id,
            region_id=region_id,
        )
        DBSession.merge(venue)
        DBSession.commit()

    #     venues.append(venue)
    #
    #     if len(venues) % pack_len == 0:
    #         DBSession.add_all(venues)
    #         DBSession.flush()
    #         DBSession.commit()
    #         venues = []
    #
    # DBSession.add_all(venues)
    # DBSession.flush()
    # DBSession.commit()


if __name__ == '__main__':
    print 'started'
    root_dir = './json/'

    limit = 1

    # cnt = 0
    # for fn in os.listdir(root_dir):
    #     print fn
    #     if cnt >= limit:
    #         break
    #     if 'categories_info' in fn:
    #         add_categories(root_dir + fn)
    #         cnt += 1

    # cnt = 0
    # for fn in os.listdir(root_dir):
    #     if cnt >= limit:
    #         break
    #     if 'events_info' in fn:
    #         add_events(root_dir + fn)
    #         cnt += 1

    # cnt = 0
    # for fn in os.listdir(root_dir):
    #     if cnt >= limit:
    #         break
    #     if 'all_subevents' in fn:
    #         add_subevents(root_dir + fn)
    #         cnt += 1

    # cnt = 0
    # for fn in os.listdir(root_dir):
    #     if cnt >= limit:
    #         break
    #     if 'all_tickets' in fn:
    #         add_tickets(root_dir + fn)
    #         cnt += 1

    cnt = 0
    for fn in os.listdir(root_dir):
        if cnt >= limit:
            break
        if 'venues_info' in fn:
            add_venues(root_dir + fn)
            cnt += 1
