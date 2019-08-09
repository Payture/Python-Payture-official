class PaytureResponse(object):
    def __init__(self, apiname, success, errormes=None, **keywarg):
        self.APIName = apiname
        self.Success = success
        self.ErrCode = errormes
        for key, value in keywarg.items():
            if key == "RedirectURL":
                self.RedirectURL = value
            elif key == "Attributes":
                self.Attributes = value
            elif key == "InternalElements":
                self.InternalElements = value
            elif key == "ListCards":
                self.ListCards = value
            elif key == "ResponseBodyXML":
                self.ResponseBodyXML = value
        super(PaytureResponse, self).__init__()

    @classmethod
    def errorResponse(cls, command, error):
        return PaytureResponse(command, False, error)
