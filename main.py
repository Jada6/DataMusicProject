import reader
import data_query
import lastfm_query


def get_data(states):
    """ Get TopArtists data from LastFM as json files """
    lastfm_query.save_lastfm_top_artists(states)


def produce_artists_country(states):
    artists_countries = reader.load_json_data("Data/ArtistsCountry.json")
    for country in states:
        artists_country = []
        for artist in top_artists[country]:
            artists_country.append(artist)
            if artist.lower() not in map(lambda x: x.lower(), artists_countries.keys()):
                print(country + " " + artist)
                artist_info = lastfm_query.MB_API_get_artist_info(artist)
                if artist_info is not None:
                    data_query.connect_artist_and_country(artist_info, artists_countries)

        reader.save_json_data(artists_country, reader.ARTISTS_COUNTRY_DIR + country + ".json")
        reader.save_json_data(artists_countries, "Data/ArtistsCountry.json")


states = reader.load_json_data("Data/country-by-population.json")
states = data_query.filter_states_by_population_limit(states, 5_000_000)
states = data_query.filter_states_without_language(states, "English")
'''
states = []
states.append("Japan")
states.append("Iran")
get_data(states)

get_data(states)  # call just once to gather TopArtists data from LastFM
'''

states = data_query.filter_states_without_music(states)
top_artists = data_query.alter_top_artists_JSON(states)


# reader.save_json_data(artists_country, "Data/australia-artists.json")

#produce_artists_country(states)


#data = reader.load_json_data("Data/ArtistsCountry/Australia.json")
#reader.save_json_data(data["Australia"], "Data/australia-artists.json")
#data = data["Australia"]

result = {}
for country in states:
    data = reader.load_json_data(reader.ARTISTS_COUNTRY_DIR + country + ".json")
    count = data_query.count_artists_from_country(data, country)
    result[country] = count

sorted_countries = sorted(result.items(), reverse=True, key=lambda x: x[1])

print([state for state in sorted_countries if state[1] != 0])
