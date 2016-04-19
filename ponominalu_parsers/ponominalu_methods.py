# coding=utf-8
import codecs
import json
import os
import requests
# from tk_constants import SESSION_ID
from ponominalu_parsers.tk_constants import SESSION_ID

__author__ = 'tkorchagin'


def get_json(method_name, params=None):
    if params is None:
        params = {}
    params['session'] = SESSION_ID
    r = requests.get("https://api.cultserv.ru/%s" % method_name, params=params)
    if '<!DOCTYPE html>' not in r.text or '<HTML>' not in r.text:
        # print r.text
        return json.loads(r.text)


def get_venues(region_id=None, everything=True, limit=10, ):
    method_name = 'v4/venues/list'
    params = {
        'region_id': region_id,
        'everything': everything,
        'limit': limit,
    }
    return get_json(method_name, params)


def get_regions(limit=10):
    method_name = 'v4/regions/list'
    params = {
        'limit': limit,
    }
    return get_json(method_name, params)


def get_categories(limit=10):
    method_name = 'v4/categories/list'
    params = {
        'limit': limit,
    }
    return get_json(method_name, params)


def get_events(category_id=None, min_price=None, max_price=None, venue_id=None,
               region_id=None, title=None, first_only=False, limit=10):
    method_name = 'v4/events/list'
    params = {
        'limit': limit,
        'category_id': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'venue_id': venue_id,
        'region_id': region_id,
        'title': title,
        'first_only': first_only,
    }
    return get_json(method_name, params)


def get_subevent(subevent_id, limit=10):
    method_name = 'v4/subevents/get'
    params = {
        'limit': limit,
        'id': subevent_id,
    }
    return get_json(method_name, params)


def get_tickets(subevent_id, sector_id, limit=10):
    method_name = 'v4/sectors/get'
    params = {
        'limit': limit,
        'subevent_id': subevent_id,
        'sector_id': sector_id,
    }
    return get_json(method_name, params)


############ FOR DB ############


def get_categories_info(categories):
    categories_info = []
    for category in categories['message']:
        category_id = category.get('id')
        alias = category.get('alias')
        title = category.get('title')

        temp = {
            'category_id': category_id,
            'alias': alias,
            'title': title,
        }
        categories_info.append(temp)
    return categories_info


def get_venues_info(venues):
    venues_info = []
    for venue in venues['message']:
        venue_id = venue.get('id')
        title = venue.get('title')
        address = venue.get('address')
        alias = venue.get('alias')
        region_id = venue.get('region_id')
        type_id = venue.get('type_id')

        temp = {
            'venue_id': venue_id,
            'title': title,
            'address': address,
            'alias': alias,
            'region_id': region_id,
            'type_id': type_id,
        }
        venues_info.append(temp)
    return venues_info


def get_subevent_info(subevent_data, event_id):
    subevent = subevent_data['message']
    if type(subevent) != dict:
        return None

    subevent_id = subevent.get('id')
    title = subevent.get('title')
    subevent_date = subevent.get('date')
    image = subevent.get('image')
    description = subevent.get('description')
    venue_id = subevent.get('venue_id')
    sectors = subevent.get('sectors', [])
    sectors_ids = [el['id'] for el in sectors]
    eticket_possible = subevent.get('eticket_possible')
    eticket_only = subevent.get('eticket_only')
    subevent_type = subevent.get('type')
    age = subevent.get('age')
    link = subevent.get('link')

    subevent_info = {
        'event_id': event_id,
        'subevent_id': subevent_id,
        'title': title,
        'subevent_date': subevent_date,
        'image': image,
        'description': description,
        'venue_id': venue_id,
        'sectors_ids': sectors_ids,
        'eticket_possible': eticket_possible,
        'eticket_only': eticket_only,
        'subevent_type': subevent_type,
        'age': age,
        'link': link,
    }
    return subevent_info


def get_events_info(events):
    events_info = []
    for event in events['message']:
        event_id = event.get('id')
        title = event.get('title')
        description = event.get('description')
        subevents = event.get('subevents', [])
        subevents_ids = [el['id'] for el in subevents]
        categories = event.get('categories')
        categories_ids = [el['id'] for el in categories]

        temp = {
            'event_id': event_id,
            'title': title,
            'description': description,
            'subevents': subevents,
            'subevents_ids': subevents_ids,
            'categories_id': categories_ids
        }
        events_info.append(temp)
    return events_info


def get_tickets_info(tickets, subevent_id):
    tickets_data = tickets['message']
    tickets_info = []
    sectior_id = tickets_data.get('id')
    sector_title = tickets_data.get('title')

    for ticket in tickets_data['content']:
        row = ticket.get('r')  # row
        number = ticket.get('n')  # number
        status = ticket.get('s')  # status: 0 - свободно, 1 - забронированно, 2 - недоступно
        price = ticket.get('p')  #
        ticket_id = ticket.get('id')

        if status == 2:
            continue

        temp = {
            'subevent_id': subevent_id,
            'sectior_id': sectior_id,
            'sector_title': sector_title,
            'row': row,
            'number': number,
            'status': status,
            'price': price,
            'ticket_id': ticket_id,
        }
        tickets_info.append(temp)
    return tickets_info


def get_regions_info(regions):
    regions_info = []
    for region in regions['message']:
        region_id = region.get('id')
        title = region.get('title')

        temp = {
            'region_id': region_id,
            'title': title,
        }
        regions_info.append(temp)
    return regions_info


def write_in_json(json_obj, fn):
    with codecs.open(fn, 'w', 'utf8') as f:
        f.write(json.dumps(json_obj, sort_keys=True, indent=4, ensure_ascii=False))


def get_and_write_all_subevents_info(events_info):
    all_subevents = []

    cnt = 0
    for event in events_info:
        event_id = event['event_id']
        subevents_ids = event['subevents_ids']
        for subevent_id in subevents_ids:
            cnt += 1
            if cnt % 25 == 0:
                print 'get_all_subevents_info', cnt

            subevent = get_subevent(subevent_id)
            subevent_info = get_subevent_info(subevent, event_id)
            if subevent_info is None:
                continue

            if cnt % 500 == 0:
                write_in_json(all_subevents, './json/all_subevents_%d.json' % cnt)
                all_subevents = []

            all_subevents.append(subevent_info)
    write_in_json(all_subevents, './json/all_subevents_%d.json' % cnt)
    return cnt


def get_all_tickets(subevents_info):
    all_tickets = []

    cnt = 0
    for subevent in subevents_info:
        subevent_id = subevent['subevent_id']
        for sector_id in subevent['sectors_ids']:
            cnt += 1
            if cnt % 10 == 0:
                print cnt
            try:
                tickets = get_tickets(subevent_id, sector_id, limit=10000)
            except Exception, e:
                continue
            all_tickets += get_tickets_info(tickets, subevent_id)
    return all_tickets


if __name__ == '__main__':
    events = get_events(limit=10000)
    print 'events', len(events['message'])
    events_info = get_events_info(events)
    write_in_json(events_info, './json/events_info.json')

    categories = get_categories(limit=10000)
    print 'categories', len(categories['message'])
    categories_info = get_categories_info(categories)
    write_in_json(categories_info, './json/categories_info.json')

    venues = get_venues(limit=1000*10000)
    print 'venues', len(venues['message'])
    venues_info = get_venues_info(venues)
    write_in_json(venues_info, './json/venues_info.json')

    events_info = json.load(open('./json/events_info.json'))
    cnt = get_and_write_all_subevents_info(events_info)
    print 'all_subevents_info', cnt

    for fn in os.listdir('./json/'):
        if 'all_subevents_' not in fn:
            continue
        all_subevents_info = json.load(open('./json/' + fn))
        q = fn[fn.rfind('_')+1:fn.rfind('.json')]
        # if q in ['1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '4845']:
        #     continue
        print fn

        all_tickets = get_all_tickets(all_subevents_info)
        print 'all_tickets', len(all_tickets)
        write_in_json(all_tickets, './json/all_tickets_%s.json' % q)

    regions = get_regions(limit=1000*1000)
    print 'regions', len(regions['message'])
    regions_info = get_regions_info(regions)
    write_in_json(regions_info, './json/regions_info.json')
