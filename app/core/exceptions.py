class ServiceException(Exception):
    def __init__(
        self,
        message: str,
        code: str = "internal_error",
        status_code: int = 500,
        details: dict = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message) 