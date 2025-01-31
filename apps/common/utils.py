import logging
import time
from functools import wraps
from typing import Callable

from django.core.cache import cache

logger = logging.getLogger(__name__)


def rate_limit(limit: int = 60, period: int = 60, key_prefix: str = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            prefix = key_prefix or func.__name__
            key = f"rate_limit:{prefix}"

            while True:
                try:
                    current_time = int(time.time())
                    window_start = current_time - period

                    requests = cache.get(key, [])
                    requests = [ts for ts in requests if ts > window_start]

                    if len(requests) < limit:
                        requests.append(current_time)
                        cache.set(key, requests, period)
                        return func(*args, **kwargs)
                    else:
                        sleep_time = requests[0] + period - current_time
                        if sleep_time > 0:
                            time.sleep(sleep_time)
                except Exception as e:
                    logger.error("Rate limit error: %s", e)
                    return func(*args, **kwargs)

        return wrapper

    return decorator
