from typing import Any

from cachetools import TTLCache


class Cache:
    """
        Simple application cache implementation. Based on TTLCache, stored in RAM memory, timed.
    Args:
        maxsize: maximal umber of items in cache
        ttl: the time-to-live value of the cache’s items.
    """

    def __init__(self, maxsize: int = 20, ttl: int = 300):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def add(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def invalidate_item(self, key: str) -> None:
        self._delete(key)

    def invalidate(self) -> None:
        self._cache.clear()

    def key_in_cache(self, key: str):
        if key in self._cache:
            return True
        return False

    def _delete(self, key: str):
        try:
            del self._cache[key]
        except KeyError:
            pass
