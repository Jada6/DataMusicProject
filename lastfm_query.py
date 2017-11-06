import urllib.request
import json
from urllib.parse import quote_plus

import reader

LAST_API_KEY = "wont tell you"  # my private Last.fm API key


def lastfm_API_top_artists_of_country(country):
    # Mustn't be more than 5requests/second averaged over a 5 minute period = 1500 requests per 5 minute
    data = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists"
                                  "&country=" + country +
                                  "&api_key=" + LAST_API_KEY +
                                  "&format=json").read()
    return json.loads(data)['topartists']['artist']


def save_lastfm_top_artists(states):
    for state in states:
        top_artists_of_country = lastfm_API_top_artists_of_country(state)
        reader.save_json_data(top_artists_of_country, reader.TOP_ARTISTS_DIR + state + ".json")


def MB_API_get_artist_info(artist):
    """ Return artist info """
    print(artist)
    url_query = u"http://musicbrainz.org/ws/2/artist/?query=artist:" \
                + quote_plus(artist.replace("~", " ")) + "&fmt=json"

    data = urllib.request.urlopen(url_query).read()

    query = json.loads(data)
    return None if len(query['artists']) == 0 else query['artists'][0]
