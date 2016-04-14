import codecs
import json
import requests

__author__ = 'tkorchagin'


def clean(s):
    s = ' '.join(s.split())
    return s


def get_events_info():
    r = requests.get("https://ticketscloud.org/v1/resources/events")
    jsonData = {'events': json.loads(r.text)}
    with codecs.open('events.json', 'w', 'utf8') as f:
        f.write(json.dumps(jsonData, sort_keys=True, indent=4, ensure_ascii=False))


def get_venues_info():
    r = requests.get("https://ticketscloud.org/v1/resources/venues")
    jsonData = {'venues': json.loads(r.text)}
    with codecs.open('venues.json', 'w', 'utf8') as f:
        f.write(json.dumps(jsonData, sort_keys=True, indent=4, ensure_ascii=False))


def parse_venues(fn):
    jsonData = json.load(open(fn))
    venues = jsonData['venues']

    cnt = 0
    for venue in venues:
        cnt += 1
        name = venue['name']
        print cnt, '"%s"' % clean(name)


def parse_events(fn):
    jsonData = json.load(open(fn))
    events = jsonData['events']

    cnt = 0
    for event in events:
        cnt += 1
        name = event['name']
        print cnt, '"%s"' % clean(name)


if __name__ == '__main__':
    print 'hi'
    parse_venues('./venues.json')
