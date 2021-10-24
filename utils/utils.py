import csv
import os
import pickle

import utils.config as conf
from utils.log import logger


def write_csv(filename, data, sort_by=None):
    if sort_by:
        data = sorted(data, key=lambda x: x[sort_by], reverse=True)
    keys = data[0].keys()
    with open('{}.csv'.format(filename), 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(data)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def retrieve_cache(filename):
    try:
        with open('{}/{}'.format(conf.CACHE_FOLDER, filename), "rb") as f:
            return pickle.load(f)
    except:
        return None

def persist_cache(filename, data):
    # Create cache folder if does not exist
    if not os.path.exists(conf.CACHE_FOLDER):
        create_folder(conf.CACHE_FOLDER)
    with open('{}/{}'.format(conf.CACHE_FOLDER, filename), "wb") as f:
        pickle.dump(data, f)
        logger.info("{} saved in cache".format(filename))
