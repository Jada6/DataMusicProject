import urllib.request
import json
import time
import os

import reader

LAST_API_KEY = "2336521f003f97f22520a74ddf198f36"


def lastfm_API_top_artists_of_country(country):
    """ Connect to Last.fm and request top 99 artists of the country
    Mustn't be more than 5requests/second averaged over a 5 minute period
    Return:
        list of dictionaries containing info about artists
        None if error in request
        [] if no statistics about country
    """
    url = u"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists" + \
          "&country=" + country.replace(" ", "%20") + \
          "&limit=99&api_key=" + LAST_API_KEY + \
          "&format=json"

    while True:
        try:
            data = urllib.request.urlopen(url).read()
            break
        except:
            print("Waiting for connection...")
            time.sleep(10)
            continue

    query = json.loads(data)
    time.sleep(0.3)
    return query['topartists']['artist'] \
        if len(query) == 1 else None  # len(query) == 3 <==> error


def save_lastfm_top_artists(states):
    """ Get TopArtists data from LastFM
    and save them as a list of ids to Data/TopArtists/country """
    for state in states:
        if os.path.exists(reader.TOP_ARTISTS_DIR + state + ".json"):
            # skip already stored countries
            continue
        top_artists_of_country = lastfm_API_top_artists_of_country(state)
        if top_artists_of_country is not None and len(top_artists_of_country) > 0:
            ids = [artist['mbid'] for artist in top_artists_of_country
                   if not artist['mbid'] == ""]
            print("Saving top artists of " + state)
            reader.save_json_data(ids, reader.TOP_ARTISTS_DIR + state + ".json")


def MB_API_get_artist_info(artist):
    """ Connect to MusicBrainz and request the artist's info
    Mustn't be more than 1 request per second
    Param artist: id representing the artist
    Return dictionary containing the artists info
    """
    url_query = u"http://musicbrainz.org/ws/2/artist/" + artist + "?fmt=json"

    while True:
        try:
            data = urllib.request.urlopen(url_query).read()
            break
        except:
            print("Waiting for connection...")
            time.sleep(10)

    time.sleep(1)

    query = json.loads(data)
    return query
