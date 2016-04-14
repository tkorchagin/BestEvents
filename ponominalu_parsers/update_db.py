import json
from sql_classes import *
from constants import *

__author__ = 'tkorchagin'

engine = create_engine(DB_PATH)
SessionClass = sessionmaker(bind=engine)
DBSession = SessionClass()


def add_events(fn, pack_len=5000):
    events = []
    cnt = 0

    events_arr = json.load(open(fn))
    events_len = len(events_arr)
    for el in events_arr:
        cnt += 1
        if cnt % 1000 == 0:
            print '%d, %.3f%%' % (cnt, 100*float(cnt)/events_len)

        event_id = el['event_id']
        title = el['title']
        link = el['link']
        print title

        event = Event(id=event_id, title=link, link=title)
        events.append(event)

        if len(event) % pack_len == 0:
            DBSession.add_all(events)
            DBSession.flush()
            DBSession.commit()
            events = []


def add_subevents(fn):
    subevents = []
    for el in json.load(open(fn))['subevents_info']:
        subevent_id = el['subevent_id']
        print subevent_id

        # str_date = el['str_date']
        # annotation = el['annotation']
        # link = el['link']
        # venue_id = el['venue_id']
        # event_id = el['event_id']
        # subevent_date = el['subevent_date']
        # commission = el['commission']
        # eticket_possible = el['eticket_possible']
        # age = el['age']
        # credit_card_payment = el['credit_card_payment']
        # sectors_list = el['sectors_list']

        if el['subevent_date'] is None or el['str_date'] is None:
            continue

        subevent = Subevent(
            id=el['subevent_id'],
            str_date=el['str_date'],
            annotation=el['annotation'],
            link=el['link'],
            subevent_date=datetime.datetime.fromtimestamp(el['subevent_date'] / 1000),
            commission=el['commission'],
            eticket_possible=el['eticket_possible'],
            age=el['age'],
            credit_card_payment=el['credit_card_payment'],
            sectors_list=el['sectors_list']
        )
        subevents.append(subevent)

    DBSession.add_all(subevents)
    DBSession.flush()
    DBSession.commit()


if __name__ == '__main__':
    print 'hello'
    fn = './json/all_events.json'
    add_events(fn)

    # fn = './json/subevents_info.json'
    # add_subevents(fn)
