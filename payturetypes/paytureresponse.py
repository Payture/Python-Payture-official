class PaytureResponse(object):

    def __init__(self, apiname, susses, errormes=None, **keywarg):
        self.APIName = apiname
        self.Success = susses
        self.ErrCode = errormes
        for key, value in keywarg.items():
            if(key == 'RedirectURL'):
                self.RedirectURL = value
            elif(key == 'Attributes'):
                self.Attributes = value
            elif(key == 'InternalElements'):
                self.InternalElements = value
            elif(key == 'ListCards'):
                self.ListCards = value
            elif(key == 'ResponseBodyXML'):
                self.ResponseBodyXML = value
        super(PaytureResponse, self).__init__()

    def errorResponse(command, error):
        return PaytureResponse( command, False, error)

