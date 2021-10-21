import os
import pickle

import utils.config as conf


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
        print("{} saved in cache".format(filename))
