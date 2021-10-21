import utils.config as conf
from locations import get_new_locations_info, parse_locations
from users import get_all_users_posts
from utils.cache import retrieve_cache
from utils.log import logger


if __name__ == "__main__":
    # Get all users posts
    logger.info("{} accounts to process".format(len(conf.ACCOUNTS)))
    posts = get_all_users_posts(conf.ACCOUNTS)
    logger.info("{} posts found".format(len(posts)))

    # Get all post locations end save them in dict
    locations = parse_locations(posts)
    logger.info("{} unique locations found".format(len(locations)))

    # Get location's metadata from cache or instagram's API
    location_cache = retrieve_cache("location_cache")
    logger.info("{} locations info in cache".format(len(location_cache)))
    if not location_cache:
        location_cache = {}
    location_cache = get_new_locations_info(locations, location_cache)
    logger.info("{} locations info".format(len(location_cache)))
