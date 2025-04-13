from fastapi import HTTPException

class InvalidStartKeyException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid start_key format")

class OrderNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Order not found")

class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized access")