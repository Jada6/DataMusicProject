import json

LANGUAGE_FILE_NAME = "Data/country-by-languages.json"
POPULATION_FILE_NAME = "Data/country-by-population.json"
TOP_ARTISTS_DIR = "Data/TopArtists/"
ARTISTS_COUNTRY_DIR = "Data/ArtistsCountry/"


def save_json_data(json_data, file_name):
    """ Save data as json file """
    with open(file_name, "w") as json_file:
        json.dump(json_data, json_file)


def load_json_data(file_name):
    """ Load data from json file """
    with open(file_name) as json_file:
        data = json.load(json_file)

    return data


