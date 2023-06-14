class FinTrackException(Exception):
    default_message = "Something went wrong"
    error_code = "ErrorCodeNotDefined"

    def __init__(self, message=None):
        self.message = message if message else self.default_message
        self.error_code = self.error_code


class NotFoundException(FinTrackException):
    message = "Not Found"
    error_code = "NotFoundException"


class AlreadyExistsException(FinTrackException):
    message = "Already Exists"
    error_code = "AlreadyExistsException"
