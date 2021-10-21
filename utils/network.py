import requests

from utils.exceptions import ClientException, ServerException
from utils.log import logger


def parse_response(response):
    if 'Content-Type' not in response.headers:
        return None
    content_type = response.headers['Content-Type'].lower()
    if 'application/json' in content_type:
        return response.json()
    elif 'text/html' in content_type:
        return response.text
    else:
        return None

def validate_requests(f):
    """
    Takes a http response
    Check if status code is valid and raise appropriate exception
    """
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        status_code = int(response.status_code)
        if status_code in [200, 201, 204]:
            return response
        raise format_request_error(status_code, f.__name__, response)
    return wrapper

def format_request_error(status_code, func_name, response):
    err = "{} Failed. Status code: {} Error: {}".format(
        func_name,
        status_code,
        parse_response(response)
    )
    logger.error(err)
    if int(status_code) in range(400, 500):
        return ClientException(status_code=status_code, details=err)
    elif int(status_code) in range(500, 600):
        return ServerException(status_code=status_code, details=err)
    return RuntimeError(status_code, err)

@validate_requests
def get_request(url, headers={}, params=None, auth=None):
    return requests.get(
        url,
        headers=headers,
        params=params,
        auth=auth
    )
