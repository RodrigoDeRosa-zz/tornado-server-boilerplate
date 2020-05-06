class BusinessError(RuntimeError):

    def __init__(self, message, status=500):
        self.message = message
        self.status = status

    def __str__(self):
        return self.message
