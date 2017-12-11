import reader
import data_query
import api_query

import matplotlib.pyplot as plt


def produce_artists_country(states):
    """ Create Data/ArtistsCountry.json
    representing the most popular artists and their country """
    # the wanted dict of artists and their countries;
    # in case there is some data stored already
    artists_countries = reader.load_json_data("Data/ArtistsCountry.json")
    top_artists = data_query.alter_top_artists_JSON(states)

    for country in states:
        for artist in top_artists[country]:
            if artist not in artists_countries.keys():
                print("Adding " + artist + " who is often listened in " + country)
                artist_info = api_query.MB_API_get_artist_info(artist)
                if artist_info is not None:
                    # sometimes it does not corespondent even if it should
                    # e.g. http://musicbrainz.org/ws/2/artist/7d2f5f88-5da7-4d94-8be4-b4fadaf5b3f6
                    if artist_info['id'] != artist:
                        artist_info['id'] = artist
                    data_query.connect_artist_and_country(artist_info, artists_countries)

            reader.save_json_data(artists_countries, "Data/ArtistsCountry.json")
            # write after every state to make sure at least
            # something is saved if there occurs a problem


def get_initial_states():
    """ Return list of strings of wanted states """
    states = reader.load_json_data("Data/country-by-population.json")
    states = data_query.filter_states_by_population_limit(states, 5_000_000)
    states = data_query.filter_states_without_language(states, "English")
    return states


def collect_data():
    """ Gather all needed data into files:
    Data/ArtistsCountry.json - dictionary of all top artists with their country,
    Data/TopArtists/country.json - list of top artists of the country.
    Return all the states included in data
    """
    states = get_initial_states()
    reader.create_dir(reader.TOP_ARTISTS_DIR)

    print("Gathering data from Last.fm")
    api_query.save_lastfm_top_artists(states)

    states = data_query.filter_states_without_music(states)

    print("Gathering data from MusicBrainz.org")
    produce_artists_country(states)

    return states


def analyze_data(states):
    """ Find the states with the most listened artists that are from the country
    (if there are more then 8 of them in the state)
    and save the data into data.json as a list of lists: [country, number of artists]
    """
    print("Analyzing data")
    # Number of artists listened in their country among the top 100
    number_of_artists_in_their_country = {}
    for country in states:
        artists_ids = reader.load_json_data(reader.TOP_ARTISTS_DIR + country + ".json")
        count = data_query.count_artists_from_country(artists_ids, country)
        number_of_artists_in_their_country[country] = count

    sorted_countries = sorted(number_of_artists_in_their_country.items(),
                              reverse=True,
                              key=lambda x: x[1])
    filtered_countries = [state for state in sorted_countries if state[1] > 8]

    reader.save_json_data(filtered_countries, reader.FINAL_DATA)


def make_graph():
    print("Making the graph")
    data = reader.load_json_data(reader.FINAL_DATA)

    values = [state[1] for state in data]
    countries = [state[0] for state in data]

    indices = [i for i in range(len(countries))]
    width = 0.8
    plt.bar(indices, values, width=width, align="center")
    plt.ylabel('Percent of artists')
    plt.title('The countries in which the most listened artists are from the country')

    plt.xticks(indices, countries, rotation=30)
    plt.tight_layout()
    plt.savefig("output.png")
    plt.show()


def main():
    states = collect_data()
    analyze_data(states)
    make_graph()


if __name__ == "__main__":
    main()
