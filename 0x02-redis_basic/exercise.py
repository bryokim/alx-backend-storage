#!/usr/bin/env python3
"""Cache module"""

import redis

from functools import wraps
from typing import Any, Callable, Optional, Union
from types import MethodType
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called.

    Args:
        method (Callable): method being called.

    Returns:
        Callable: Wrapper function that increments the count and returns
            the called method.
    """

    @wraps(method)
    def wrapper(*args, **kwargs) -> Callable:
        args[0]._redis.incr(method.__qualname__)
        return method(*args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs of a particular method.

    Args:
        method (Callable): method being called.

    Returns:
        Callable: Wrapper function that pushes the inputs and outputs
            to their respective lists and returns output of the method.
    """

    @wraps(method)
    def wrapper(*args, **kwargs):
        args[0]._redis.rpush(f"{method.__qualname__}:inputs", str(args[1:]))
        output = method(*args, **kwargs)
        args[0]._redis.rpush(f"{method.__qualname__}:outputs", str(output))

        return output

    return wrapper


class Cache:
    """Cache class"""

    def __init__(self) -> None:
        """Initialize new Cache"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """Stores data in Redis using a random key and returns the key.

        Args:
            data (Union[str, int, float, bytes]): Data to store in Redis.

        Returns:
            str: Key associated with the data.
        """

        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], Any]] = None
    ) -> Any:
        """Gets a value based on the key from the Redis server.
        If `fn` is not None, then it's used to convert the value to the
        desired format.

        Args:
            key (str): Key of the value to get.
            fn (Optional[Callable[[bytes], Any]]): Callable to convert the
                value to desired format.

        Returns:
            Any: Value in the desired format, or bytes if `fn` is not provided.
                `None` is returned if the key is not found.
        """
        value = self._redis.get(key)
        if value is None:
            return None

        if fn:
            value = fn(value)

        return value

    def get_int(self, key: str) -> Optional[int]:
        """Get an integer value.

        Args:
            key (str): Key of the value to get.

        Returns:
            int: Value as an integer, or None if key is not found.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Optional[str]:
        """Get string value.

        Args:
            key (str):Key of the value to get.

        Returns:
            str: Value as a str, or None if key is not found.
        """
        return self.get(key, str)


def replay(fn: Any) -> None:
    """Displays history of calls of a particular function.

    Args:
        fn (Any): Function to display its history.
    """

    r = fn.__self__._redis
    name = fn.__qualname__

    count = int(r.get(name))
    print("{} was called {} times:".format(name, count))

    for input, output in zip(
        r.lrange(f"{name}:inputs", 0, -1), r.lrange(f"{name}:outputs", 0, -1)
    ):
        print(
            "{}(*{}) -> {}".format(
                name, input.decode("utf-8"), output.decode("utf-8")
            )
        )
