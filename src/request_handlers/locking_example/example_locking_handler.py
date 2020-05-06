from asyncio import sleep

from src.model.errors.etcd_errors import ExistingLockError
from src.request_handlers.custom_request_handler import CustomRequestHandler
from src.utils.concurrency.lock_manager import LockManager


class ExampleLockingHandler(CustomRequestHandler):

    SUPPORTED_METHODS = ['GET']

    async def get(self, lock_id):
        """ Example of a request handling where we need to acquire a lock. """
        try:
            LockManager.get().acquire(lock_id)
            await sleep(5)
            self.make_response({'aLock': lock_id})
            LockManager.get().release(lock_id)
        except ExistingLockError:
            message = f'Lock id {lock_id} is currently being used. Please try later.'
            self.make_error_response(message=message, status_code=409)
