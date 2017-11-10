

class Error(Exception):

    def __init__(self, detail=None):
        self.detail = None


class MissingRequiredParam(Error):
    pass


class RequestPaymentFail(Error):
    pass


class RequestQueryFail(Error):
    pass
