# coding=utf-8
import codecs
import json
import requests
from tk_constants import *

__author__ = 'tkorchagin'


def get_all_events(all_number=2000):
    method_name = 'get_all_events'
    limit = 200
    data = {
        'session': SESSION_ID,
        'limit': limit,
    }

    final_data = []

    for q in xrange(all_number / limit):
        offset = q * limit
        print offset

        data['offset'] = offset
        r = requests.post("http://api.cultserv.ru/jtransport/partner/%s" % method_name, data=data)
        json_response = json.loads(r.text)

        for event in json_response['message']:
            event_id = event.get('id', 0)
            title = event.get('title', '')
            link = event.get('link', '')
            subevents = event.get('subevents', [])
            subevents_ids = [el.get('id') for el in subevents]

            temp = {
                'event_id': event_id,
                'title': title,
                'link': link,
                'subevents_ids': subevents_ids
            }
            final_data.append(temp)
    return final_data


def get_json(method_name, data=None):
    if data is None:
        data = {}
    data['session'] = SESSION_ID
    r = requests.get("http://api.cultserv.ru/jtransport/partner/%s" % method_name, params=data)
    if '<!DOCTYPE html>' not in r.text:
        return json.loads(r.text)


def get_venues(title):
    method_name = 'get_venues'
    print 'method: "%s"' % method_name

    data = {
        'title': title,
        'limit': 10,
    }

    jsonData = get_json(method_name, data)
    if jsonData['message']:
        theatre_id = jsonData['message'][0]['id']
        return theatre_id


def get_venue(venue_id):  # Возвращает json с нужными полями о театре
    method_name = 'get_venue'
    print 'method: "%s"' % method_name

    data = {'id': venue_id}
    jsonData = get_json(method_name, data)
    return jsonData


def get_actual_events_ids_only():
    method_name = 'get_actual_events_ids_only'
    print 'method: "%s"' % method_name

    # data = {'etickets_only': True}
    data = {}

    jsonData = get_json(method_name, data)
    return jsonData


def get_events(category=THEATRE_CATEGORY_ID, min_date='2016-04-01'):
    method_name = 'get_events'
    print 'method: "%s"' % method_name

    data = {
        'category': category,
        'min_date': min_date,
        # 'one_for_event': True,
    }

    jsonData = get_json(method_name, data)
    return jsonData


def get_subevent(event_id):
    method_name = 'get_subevent'
    print 'method: "%s"' % method_name

    data = {
        'id': event_id,
    }

    jsonData = get_json(method_name, data)
    return jsonData


def get_sector(sector_id):
    method_name = 'get_sector'

    data = {
        'sector_id': sector_id,
    }

    jsonData = get_json(method_name, data)
    return jsonData


def get_tickets(subevent_id, sector_id):
    method_name = 'get_tickets'
    print 'method: "%s"' % method_name

    data = {
        'subevent_id': subevent_id,
        'sector_id': sector_id,
    }

    jsonData = get_json(method_name, data)
    return jsonData


def get_best_tickets(subevent_id, sector_id, quantity, min_price=0, max_price=100000):
    method_name = 'get_best_tickets'
    print 'method: "%s"' % method_name

    data = {
        'subevent_id': subevent_id,
        'sector_id': sector_id,
        'quantity': quantity,
        'min_price': min_price,
        'max_price': max_price,
    }

    jsonData = get_json(method_name, data)
    return jsonData


def get_events_info(fn):
    print 'get_events_info'
    print fn
    final = []

    jsonData = json.load(open(fn))
    for item in jsonData['message']:
        title = item['title']
        event_id = item['id']
        # event_dates = [datetime.datetime.fromtimestamp(q/1000.0) for q in item['event']['dates']]
        event_dates = item['event']['dates']
        event_img_url = 'http://media.cultserv.ru/library/original/%s' % item['original_image']
        venue_id = item['venue']['id']
        venue_title = item['venue']['title']

        event_data = {
            'title': title,
            'event_id': event_id,
            'event_dates': event_dates,
            'event_img_url': event_img_url,
            'venue_id': venue_id,
        }

        print '%d -- "%s" -- "%s"' % (event_id, venue_title, title)

        final.append(event_data)
    jsonData = {'events_info': final}
    return jsonData


def get_subevents_info(fn, limit=10):
    print 'get_subevents_info'

    final = []

    jsonData = json.load(open(fn))
    cnt = 0
    for event in jsonData:
        cnt += 1
        if cnt > limit:
            break
        event_id = event['event_id']
        for subevent_id in event['subevents_ids']:
            subevent = get_subevent(subevent_id)

            subevent_data = subevent.get('message')
            if type(subevent_data) != dict:
                print 'passed message:', subevent_data
                continue

            commission = subevent_data.get('commission', 0)
            eticket_possible = subevent_data.get('eticket_possible', False)
            age = subevent_data.get('age', 0)
            credit_card_payment = subevent_data.get('credit_card_payment', False)
            sectors = subevent_data.get('sectors', [])
            sectors_list = [q['id'] for q in sectors]
            subevent_date = subevent_data['date']
            venue_id = subevent_data.get('venue_id')
            link = subevent_data.get('link')
            annotation = subevent_data.get('annotation')
            str_date = subevent_data.get('str_date')

            subevent_info = {
                'str_date': str_date,
                'annotation': annotation,
                'link': link,
                'venue_id': venue_id,
                'event_id': event_id,
                'subevent_id': subevent_id,
                'subevent_date': subevent_date,
                'commission': commission,
                'eticket_possible': eticket_possible,
                'age': age,
                'credit_card_payment': credit_card_payment,
                'sectors_list': sectors_list,
            }

            # print subevent_info
            final.append(subevent_info)
    jsonData = {'subevents_info': final}
    return jsonData


def get_tickets_info(fn, limit=10):
    print 'get_tickets_info'

    final = []
    jsonData = json.load(open(fn))
    for item in jsonData['subevents_info'][:limit]:
        subevent_id = item['subevent_id']
        for sector_id in item['sectors_list']:
            tickets = get_tickets(subevent_id, sector_id)
            if tickets is None:
                continue
            for t in tickets.get('message', []):
                price = t.get('price')
                seat = t.get('seat')
                ticket_id = t.get('id')
                row = t.get('row')

                if None in [price, seat, ticket_id, row]:
                    continue

                temp = {
                    'subevent_id': subevent_id,
                    'sector_id': sector_id,
                    'price': price,
                    'seat': seat,
                    'ticket_id': ticket_id,
                    'row': row
                }
                final.append(temp)

    jsonData = {'tickets_info': final}
    return jsonData


def get_venues_info(fn, limit=10):
    print 'get_venues_info'

    final = []
    distinct_venues = []
    jsonData = json.load(open(fn))
    for subevent_info in jsonData['subevents_info'][:limit]:
        venue_id = subevent_info.get('venue_id')
        if venue_id is None:
            continue
        if venue_id not in distinct_venues:
            distinct_venues.append(venue_id)
        else:
            continue

        venue = get_venue(venue_id)
        venue_info = venue['message']
        address = venue_info.get('address', '')
        description = venue_info.get('description', '')
        eng_title = venue_info.get('eng_title')
        google_address = venue_info.get('google_address')
        title = venue_info.get('title')
        type = venue_info.get('type')
        region_id = venue_info.get('region_id')
        image_global = venue_info.get('image_global')

        temp = {
            'venue_id': venue_id,
            'address': address,
            'description': description,
            'eng_title': eng_title,
            'google_address': google_address,
            'title': title,
            'type': type,
            'region_id': region_id,
            'image_global': image_global,
        }

        final.append(temp)
    jsonData = {'venues_info': final}
    return jsonData


def write_in_json(json_obj, fn):
    with codecs.open(fn, 'w', 'utf8') as f:
        f.write(json.dumps(json_obj, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    print 'parsers started'

    json_root = './json/'
    # all_events = get_all_events(all_number=1000)
    # write_in_json(all_events, json_root + 'all_events.json')

    # subevents_info = get_subevents_info(json_root + 'all_events.json', limit=1000)
    # write_in_json(subevents_info, json_root + 'subevents_info.json')

    # venues_info = get_venues_info(json_root + 'subevents_info.json', limit=1000)
    # write_in_json(venues_info, json_root + 'venues_info.json')

    tickets_info = get_tickets_info(json_root + 'subevents_info.json', limit=1000)
    write_in_json(tickets_info, json_root + 'tickets_info.json')
