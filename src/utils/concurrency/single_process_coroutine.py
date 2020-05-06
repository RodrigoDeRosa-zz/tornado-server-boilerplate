from functools import wraps

from src.utils.concurrency.lock_manager import LockManager


def single_process_coroutine(lock_name):
    """ This executes a coroutine only if there is no other process executing it. """
    def decorator(f):
        @wraps(f)
        async def locked_coroutine(*args, **kwargs):
            if LockManager.get().acquire(lock_name, blocking=False, silent=True):
                try:
                    return await f(*args, **kwargs)
                finally:
                    LockManager.get().release(lock_name)
        return locked_coroutine
    return decorator
