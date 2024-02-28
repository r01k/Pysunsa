class PysunsaError(Exception):
    """Raised when Pysunsa request ends in error.
    Attributes:
        status_code - error code returned by the Sunsa API
        status - more detailed description
    """

    def __init__(self, status_code, status):
        self.status_code = status_code
        self.status = status
