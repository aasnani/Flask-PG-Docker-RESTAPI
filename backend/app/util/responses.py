# Standardized response object
class BaseResponse(object):
    def __init__(self, message: str):
        self.message = message

    def toDict(self) -> dict:
        return self.__dict__