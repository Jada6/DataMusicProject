import urllib.request
import json
from urllib.parse import quote_plus
import time

import reader

LAST_API_KEY = "2336521f003f97f22520a74ddf198f36"  # my private Last.fm API key


def lastfm_API_top_artists_of_country(country):
    # Mustn't be more than 5requests/second averaged over a 5 minute period = 1500 requests per 5 minute
    data = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists"
                                  "&country=" + country +
                                  "&api_key=" + LAST_API_KEY +
                                  "&format=json").read()
    query = json.loads(data)
    return query['topartists']['artist'] if len(query) == 1 else None  # len(query) == 3 <==> error


def save_lastfm_top_artists(states):
    for state in states:
        top_artists_of_country = lastfm_API_top_artists_of_country(state)
        time.sleep(0.5)
        print(state)
        if top_artists_of_country is not None:
            reader.save_json_data(top_artists_of_country, reader.TOP_ARTISTS_DIR + state + ".json")


def MB_API_get_artist_info(artist):
    """ Return artist info """
    # Mustn't be more than 1 request per second
    url_query = u"http://musicbrainz.org/ws/2/artist/?query=artist:" \
                + quote_plus(artist.replace("~", " ").replace("/", " ").replace("[", "").replace("]", "")) + "&fmt=json"

    data = urllib.request.urlopen(url_query).read()

    query = json.loads(data)
    time.sleep(1)
    return None if len(query['artists']) == 0 else query['artists'][0]
