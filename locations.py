import time
from collections import defaultdict
from random import randint

import utils.config as conf
from connectors.instagramConnector import fetch_one_location
from utils.log import logger
from utils.utils import persist_cache, retrieve_cache


def get_new_locations_info(locations, cache):
    """
    If a location is not in cache and has been visited more than $minimum_visits times
    Request instagram's API
    Save data in cache
    """
    for i, (id, nb_tags) in enumerate(locations.items()):
        if id in cache:
            logger.debug("{}/{}. Name: {} Nb tags: {} - already in cache".format(i, len(locations), cache[id]["name"] if "name" in cache[id] else "", nb_tags))
            continue
        if nb_tags < conf.MINIMUM_LOCATION_VISITS:
            continue
        logger.info("{}/{}. Id: {}  Nb tags:{}".format(i, len(locations), id, nb_tags))
        #continue
        cache[id] = fetch_one_location(id)
        persist_cache("location_cache", cache)
        # Random sleep between each request to instagram's API
        time.sleep(randint(conf.REQUEST_SLEEP_RANGE[0], conf.REQUEST_SLEEP_RANGE[1]))
    return cache

def parse_locations(posts):
    """
    Go through all the posts
    keep only posts with a location tagged
    Save data in a dict and count the number of posts for each location
    """
    locations = defaultdict(int)
    for post in posts:
        # Ignore posts without location
        if not post["location"]:
            continue
        locations[post["location"]['id']] += 1
    return locations
