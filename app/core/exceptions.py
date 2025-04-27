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

class ResourceNotFound(ServiceException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with id {resource_id} not found",
            code="resource_not_found",
            status_code=404
        )

class DuplicateResource(ServiceException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="duplicate_resource",
            status_code=409
        ) 