import os

import reader


def filter_states_by_population_limit(data, limit):
    """ Return states with population higher than limit """
    return [state for state in data if state['population'] >= limit]


def alter_country_by_languages_JSON(states):
    """ Return new dictionary where every state is key and its value is list of its languages """
    #states = Reader.load_json_data(Reader.LANGUAGE_FILE_NAME)
    new_states = {}

    for record in states:
        state_name = record['country']
        if state_name not in new_states:
            new_states[state_name] = []
        new_states[state_name].append(record['language'])

    return new_states


def filter_states_without_music(states):
    return [state for state in states if os.path.exists(reader.TOP_ARTISTS_DIR + state + ".json")]


def filter_states_without_language(states, language):
    """ Return list of states without the language as official language """
    states = [state['country'] for state in states]
    states_by_language = alter_country_by_languages_JSON(reader.load_json_data(reader.LANGUAGE_FILE_NAME))

    return [state for state in states
            if state in states_by_language
            and language not in states_by_language[state]]


def list_of_nonengland_artist(nonengland_artists, new_artists):
    """ Take dictionary of nonengland artists and add new from list of new artists"""


def connect_artist_and_country(artist_info, artists_country):
    """
    Writes Artist and their country into dictionary
    :param artist_info:
    :param artists_country:
    :return:
    """

    artists_country[artist_info['name']] = artist_info['area']['name'] if 'area' in artist_info else "Unknown"


def alter_top_artists_JSON(states):
    result = {}
    for state in states:
        top_artists = reader.load_json_data(reader.TOP_ARTISTS_DIR + state + ".json")
        top_artists2 = [artist['name'] for artist in top_artists]
        result[state] = top_artists2

    '''
    result[state] = ([artist['name'] for artist in top_artists_of_country])
    top_artists_of_country.append(top_artist[])
    '''
    return result


def get_country_of_artist(artist):
    artists_country = reader.load_json_data("Data/ArtistsCountry.json")
    return artists_country[artist] if artist in artists_country else "Unknown"


def count_artists_from_country(artists, country):
    result = 0
    for artist in artists:
        artist_country = get_country_of_artist(artist)
        if country == artist_country:
            result += 1

    return result
