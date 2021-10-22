import json
import time
from random import randint

import utils.config as conf
from utils.log import logger
from utils.network import get_request


def fetch_one_location(location_id):
    """
    From a location id fetch data from instagram's API
    Remove unused attributes of the location
    Return location data
    """
    headers = {
        'cookie': conf.COOKIE
    }
    params = (
        ('__a', '1'),
    )
    url = 'https://www.instagram.com/explore/locations/{location_id}/'.format(location_id=location_id)
    response = get_request(url=url, headers=headers, params=params)
    response = response.json()["native_location_data"]["location_info"]
    # Delete unused keys
    for key in ("ig_business", "hours", "has_menu", "num_guides", "show_location_page_survey"):
        response.pop(key, None)
    return response

def fetch_one_user_profile_page(slug):
    """
    Get instagram user's profile page
    Necessary to get the 12 first posts and the offset to start looping over posts
    """
    headers = {
        'cookie': conf.COOKIE
    }
    params = (
        ('__a', '1'),
    )
    url = 'https://www.instagram.com/{slug}/'.format(slug=slug)
    response = get_request(url=url, headers=headers, params=params)
    try:
        return response.json()['graphql']['user']['edge_owner_to_timeline_media']
    except:
        logger.error("Cannot get {} profile page. Status: {} Error: {}".format(slug, response.status_code, response.text))
        return None

def fetch_user_all_posts(slug, user_id, offset, posts):
    """
    Get all instagram user's posts
    """
    headers = {
        'cookie': conf.COOKIE
    }
    params = (
        ('query_hash', conf.QUERY_HASH),
        ('variables',  json.dumps({
            "id": user_id,
            "first": conf.POSTS_PER_PAGE,
            "after": offset
        }))
    )
    # If first query, get user's profile page
    if not offset:
        response = fetch_one_user_profile_page(slug)
        if not response:
            return None
    # Else get only posts (starting from the offset)
    else:
        url = 'https://www.instagram.com/graphql/query/'
        response = get_request(url=url, headers=headers, params=params)
        response = response.json()['data']['user']['edge_owner_to_timeline_media']

    offset = response["page_info"]["end_cursor"]
    posts += [x["node"] for x in response["edges"]]
    # Loop until there is no more page to download
    if response["page_info"]["has_next_page"] == True:
        logger.debug("{}/{}".format(len(posts), response["count"]))
        # Random sleep between each request to instagram's API
        time.sleep(randint(conf.REQUEST_SLEEP_RANGE[0], conf.REQUEST_SLEEP_RANGE[1]))
        return fetch_user_all_posts(slug, user_id, offset, posts)
    return posts
