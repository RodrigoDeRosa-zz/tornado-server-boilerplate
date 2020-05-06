class ExistingLockError(RuntimeError):

    def __init__(self, lock_id):
        self.message = f'Currently using lock with id {lock_id}.'

    def __str__(self):
        return self.message


class EtcdConnectionError(RuntimeError):

    def __init__(self, port):
        self.message = f'Failed to connect to etcd server in port {port}.'

    def __str__(self):
        return self.message
