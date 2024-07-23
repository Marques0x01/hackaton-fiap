class UsernameAlreadyExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"User already exists: {self.message}"



class ErrorOnConfirmingUser(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Error on confirming user: {self.message}"


class EntityNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Data not found: {self.message}"