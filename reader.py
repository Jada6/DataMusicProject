import json
import os

LANGUAGE_FILE_NAME = "Data/country-by-languages.json"
POPULATION_FILE_NAME = "Data/country-by-population.json"
TOP_ARTISTS_DIR = "Data/TopArtists/"
FINAL_DATA = "Data/final-data.json"


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def save_json_data(json_data, file_name):
    """ Save data as json file """
    with open(file_name, "w") as json_file:
        json.dump(json_data, json_file, )


def load_json_data(file_name):
    """ Load data from json file """
    if not os.path.exists(file_name):
        open(file_name, 'w')
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data
