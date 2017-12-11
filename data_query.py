import os

import reader


def filter_states_by_population_limit(data, limit):
    """ Return states with population higher than limit """
    return [state for state in data if state['population'] >= limit]


def alter_country_by_languages(states):
    """ Return new dictionary where key is state
    and its value is a list of all its languages """
    new_states = {}

    for record in states:
        state_name = record['country']
        if state_name not in new_states:
            new_states[state_name] = []
        new_states[state_name].append(record['language'])

    return new_states


def filter_states_without_music(states):
    """ Filter those countries which don't have statistics on Last.fm """
    return [state for state in states
            if os.path.exists(reader.TOP_ARTISTS_DIR + state + ".json")]


def filter_states_without_language(states, language):
    """ Return list of states without the language as official language """
    states = [state['country'] for state in states]
    states_by_language = alter_country_by_languages(reader.load_json_data(reader.LANGUAGE_FILE_NAME))

    return [state for state in states
            if state in states_by_language
            and language not in states_by_language[state]]


def connect_artist_and_country(artist_info, artists_country):
    """ Write Artist and their country into param artists_country
    Artist_info - dictionary containing info about artist """
    state_code = artist_info['country'] if 'country' in artist_info else "Unknown"
    result = get_state_name(state_code) if state_code is not None else "Unknown"
    artists_country[artist_info['id']] = result


def get_state_name(state_code):
    """ Return long name of the state, None if the code doesn't exist """
    # codes - list of dicts with keys Code and Name
    codes = reader.load_json_data("Data/state_codes.json")

    result = [state["Name"] for state in codes if state["Code"] == state_code]
    return None if len(result) == 0 else result[0]


def alter_top_artists_JSON(states):
    """ Collect and return all data about top artists into one dictionary:
    key - state, values - top artists of the state
    """
    result = {}
    for state in states:
        top_artists = reader.load_json_data(reader.TOP_ARTISTS_DIR + state + ".json")
        result[state] = top_artists

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
