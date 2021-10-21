from connectors.instagramConnector import fetch_user_all_posts
from utils.cache import persist_cache, retrieve_cache
from utils.log import logger


def get_all_users_posts(accounts):
    """
    Download all posts of users
    If already exists in cache no need to download them again
    If not in cache, download all of them and save in cache
    """
    all_posts = []
    for i, (slug, id) in enumerate(accounts):
        logger.debug("{}/{}. {}".format(i, len(accounts), slug))
        # Check if in cache
        posts = retrieve_cache(slug)
        if not posts:
            logger.info("{}/{}. {} Not in cache".format(i, len(accounts), slug))
            #continue
            posts = fetch_user_all_posts(slug, id, None, [])
            persist_cache(slug, posts)
        all_posts += posts
    return all_posts
