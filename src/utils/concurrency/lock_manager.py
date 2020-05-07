from etcd import Client, Lock, EtcdKeyNotFound, EtcdConnectionFailed

from src.model.errors.etcd_errors import ExistingLockError, EtcdConnectionError
from src.server.application_context import LockServerData
from src.utils.logging.logger import Logger


class LockManager:

    INSTANCE = None

    def __init__(self, lock_server_data: LockServerData):
        if not lock_server_data.enabled: return
        # Only set up connection if it's enabled
        self.client = self.__create_client(lock_server_data.host, lock_server_data.port)
        self.own_lock = Lock(self.client, 'manager-lock')
        self.locks = dict()
        self.set(self)

    def acquire(self, lock_id, blocking=True, silent=False):
        """ Create and lock an etcd lock. """
        return self.__create(lock_id, silent) and self.__lock(lock_id, blocking)

    def release(self, lock_id):
        """ Unlock and destroy an etcd lock. """
        self.__unlock(lock_id)
        self.__destroy(lock_id)

    def __create(self, lock_id, silent) -> bool:
        """ Create an etcd lock. Fails if it already exists. The idea is to create-and-destroy when needed. """
        self.own_lock.acquire(blocking=True)  # This is a problem as it blocks all coroutines (but it is a short block)
        try:
            self.client.read(lock_id)
        except EtcdKeyNotFound:
            # We could write whatever we wanted here, we only care about the key's existence
            self.client.write(lock_id, 'on')
            self.locks[lock_id] = Lock(self.client, lock_id)
            return True
        finally:
            self.own_lock.release()
        # If the key existed, then we don't want to lock.
        if not silent: raise ExistingLockError(lock_id)
        else: return False

    def __destroy(self, lock_id):
        """ Remove a lock from the dictionary and from the etcd server. """
        self.client.delete(lock_id)
        self.locks.pop(lock_id)

    def __lock(self, lock_id, blocking=True) -> bool:
        """ Acquire a lock with given id. Be sure to create it before acquiring it. """
        return self.locks[lock_id].acquire(blocking=blocking)

    def __unlock(self, lock_id):
        """ Release a lock with given id. Be sure to create and acquire it before releasing it. """
        self.locks[lock_id].release()

    @classmethod
    def __create_client(cls, etcd_host, etcd_port) -> Client:
        """ Create etcd client and test connection. """
        Logger(cls.__name__).info('Connecting to etcd server...')
        client = Client(host=etcd_host, port=etcd_port)
        # Test connection by trying to read a random value
        try:
            client.read('nodes')
        except EtcdConnectionFailed:
            raise EtcdConnectionError(port=etcd_port)
        except EtcdKeyNotFound:
            # This is to handle the case where etcd did not have the key (we don't care) but it is running
            pass
        return client

    @classmethod
    def set(cls, instance):
        cls.INSTANCE = instance

    @classmethod
    def get(cls):
        return cls.INSTANCE
