# by Richi Rod AKA @richionline / falken20
# ./falken_plants/cache.py

from datetime import datetime

from .logger import Log
from .config import get_settings

Log.info("***** Loading cache.py")

previous_cache = datetime.now()


def check_cache(seconds: int = 3600):  # 60 minutes default
    # Cache info:
    # hits is the number of calls that @lru_cache returned directly from memory because they existed in the cache.
    # misses is the number of calls that didn’t come from memory and were computed.
    # maxsize is the size of the cache as you defined it with the maxsize attribute of the decorator.
    # currsize  is the current size of the cache.
    global previous_cache
    # Log.info(f"CACHE calendar_data(): {calendar_data.cache_info()}")
    Log.info(
        f"CACHE get_settings(): {get_settings.cache_info()}")
    Log.info(
        f"Checking expiration time for cache({seconds=})...")
    Log.debug(f"Previous cache: {previous_cache}")
    Log.debug(f"Current time: {datetime.now()}")
    difference = (datetime.now() - previous_cache).seconds
    Log.info(
        f"Cache span: {int(difference)} seconds ({int(difference / 60)} minutes)")
    if difference > seconds:
        Log.info("Cleaning cache by expiration...")
        # calendar.cache_clear()
        previous_cache = datetime.now()
        # Log.info(f"CACHE: {calendar.cache_info()}")
