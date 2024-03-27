#!/usr/bin/env python3

"""
Defines a Cache clas that utilizes Redis for caching data
"""

import uuid
import redis
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator function to count the number of times a method is called

    Args:
        method: The method to be decorated

    Returns:
        Callable: The decorated method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator function to store the history of inputs
    and outputs for a function

    Args:
        method: The method to be decorated

    Returns:
        Callable: The decorated method
    """
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


def replay(func: Callable) -> None:
    """
    Function to display the history of calla of a particular function

    Args:
        func: function whose call history needs to be displayed

    Returns:
        None
    """
    func_name = func.__qualname__

    # Retrieve inputs and outputs from Redis lists
    inputs = cache._redis.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(func_name), 0, -1)

    # Print the history of calls
    print(f"{func_name} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{func_name}(*{inp}) -> {out.decode('utf-8')}")


class Cache:
    """
    A class for caching data using Redis
    """

    def __init__(self):
        """
        Initializes the Cache object with a Redis client
        and flushes the Redis instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a random key and
        returns the key

        Args:
            data: data stored in the cache

        Returns:
            str: The randomly generated key used to store
            the data in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    @count_calls
    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int,
                                                          float, None]:
        """
        Retrieves data form Redis using the given key and optionally
        applies a conversion function

        Args:
            key: The key associated with the data in the cache
            fn: Optional conversion function to be applied to the
            retrieved data

        Returns:
            Union[str, bytes, int, float, None]: Retrieved data
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    @count_calls
    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves a string value from redis using the given key

        Args:
            key: The key associated with the string value in the cache

        Returns:
            Union[str, None]: The retrieved string value
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    @count_calls
    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer value from redis using the given key

        Args:
            key: The key associated with the integer value in the cache

        Returns:
            Union[str, None]: The retrieved integer value
        """
        return self.get(key, fn=int)
