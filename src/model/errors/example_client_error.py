class ExampleClientError(RuntimeError):

    def __init__(self, message):
        self.message = f'Failed to retrieve information from client. Error: {message}'

    def __str__(self):
        return self.message
