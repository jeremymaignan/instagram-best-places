class baseException(Exception):
    def __init__(self, status_code, details):
        self.status_code = status_code
        self.details = details

class ClientException(baseException):
    def __init__(self, details, status_code=400):
        self.status_code = status_code
        self.details = details

class ServerException(baseException):
    def __init__(self, details, status_code=500):
        self.status_code = status_code
        self.details = details
