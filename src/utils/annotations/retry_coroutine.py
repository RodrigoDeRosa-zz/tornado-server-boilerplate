from functools import wraps

from tornado.gen import sleep


def retry_coroutine(exceptions, attempts=4, delay=1, back_off=1):
    """ Decorates a coroutine and makes the given number of attempts, catching only the given
     exceptions. The exceptions parameter could be a tuple of exception classes or a single class. """
    def decorator(f):
        @wraps(f)
        async def retry_function(*args, **kwargs):
            """ Do function execution. """
            tries_left, wait = attempts, delay
            while tries_left > 1:
                try:
                    return await f(*args, **kwargs)
                except exceptions:
                    await sleep(wait)
                    tries_left -= 1
                    wait *= back_off
            return await f(*args, **kwargs)
        return retry_function
    return decorator
