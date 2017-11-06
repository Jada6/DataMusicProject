import reader
import data_query
import lastfm_query
import time


def get_data(states):
    """ Get TopArtists data from LastFM as json files """
    lastfm_query.save_lastfm_top_artists(states)


states = reader.load_json_data("Data/country-by-population.json")
states = data_query.filter_states_by_population_limit(states, 10_000_000)
states = data_query.filter_states_without_language(states, "English")

# get_data(states)  # call just once to gather TopArtists data from LastFM

top_artists = data_query.alter_top_artists_JSON(states)
artists_country = {}

for artist in top_artists["Australia"][20:]:
    if artist not in artists_country:
        artist_info = lastfm_query.MB_API_get_artist_info(artist)
        if artist_info is not None:
            data_query.connect_artist_and_country(artist_info, artists_country)
        time.sleep(1)
print(artists_country)


