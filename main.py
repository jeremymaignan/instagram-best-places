import utils.config as conf
from locations import get_new_locations_info, parse_locations
from users import get_all_users_posts
from utils.log import logger
from utils.utils import retrieve_cache, write_csv


def sort_locations(location_cache, locations):
    """
    Sort locations by by categories (cities, countries, restaurants, hotels and others)
    Ignore location tagged less than MINIMUM_LOCATION_VISITS times or without name
    """
    sorted_locations = {
        "cities": [],
        "countries": [],
        "restaurants": [],
        "hotels": [],
        "others": []
    }

    for id, nb_tags in locations.items():
        if nb_tags < conf.MINIMUM_LOCATION_VISITS:
            continue
        # Ignore location not in cache of without name
        if id not in location_cache or 'name' not in location_cache[id]:
            continue

        # Parse name, city and category of each location
        name = location_cache[id]["name"]
        city = location_cache[id]["location_city"] if "location_city" in location_cache[id] else ""
        if "category" in location_cache[id]:
            category = location_cache[id]["category"]
            category = conf.CATEGORY_TRANSLATIONS.get(category, category)
        # Sort cities
        if category == 'City':
            sorted_locations["cities"].append({
                "name": name,
                "count": nb_tags
            })
        # Sort countries
        elif category == 'Country/Region':
            sorted_locations["countries"].append({
                "name": name,
                "count": nb_tags
            })
        # Sort restaurants
        elif category in conf.RESTAURANT_CATEGORIES or "restaurant" in category.lower():
            sorted_locations["restaurants"].append({
                "name": name,
                "count": nb_tags,
                "category": category,
                "city": city
            })
        # Sort bars
        elif category in conf.HOTEL_CATEGORIES or "hotel" in category.lower():
            sorted_locations["hotels"].append({
                "name": name,
                "count": nb_tags,
                "category": category,
                "city": city
            })
        # Sort other categories
        else:
            sorted_locations["others"].append({
                "name": name,
                "count": nb_tags,
                "category": category,
                "city": city
            })
    return sorted_locations

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

    # Sort most visitied cities, countries, restaurants, other categories
    sorted_locations = sort_locations(location_cache, locations)

    # Format output (CSV files)
    for key, data in sorted_locations.items():
        write_csv(key, data, sort_by="count")
