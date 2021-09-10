from fastapi import HTTPException

class GlobalException(HTTPException):
  def __init__(self, status_code: int, message: str):
    self.status_code = status_code
    self.message = message

    super().__init__(status_code=self.status_code, detail=self.message)