#!/usr/bin/env python3
"""get_page module"""

import redis
import requests

from functools import wraps
from typing import Callable

cache = redis.Redis()


def url_count(fn: Callable) -> Callable:
    """Count number of times a url has been requested.
    The count is added to cache and expires after 10 seconds

    Args:
        fn (Callable): Function being decorated.
    Returns:
        Callable: Function that counts number of times url is
            requested and returns the called function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs) -> Callable:
        if args:
            url = args[0]
        elif kwargs:
            url = kwargs.get("url")

        cache.incr(f"count:{url}")
        result = cache.get(f"cache:{url}")

        if result:
            return result.decode("utf-8")

        result = fn(*args, **kwargs)
        cache.setex(f"cache:{url}", 10, result)
        return result

    return wrapper


@url_count
def get_page(url: str) -> str:
    """Get a web page.

    Args:
        url (str): Url of the page to get.
    Returns:
        str: Content of the page.
    """
    r = requests.get(url)

    return r.text
