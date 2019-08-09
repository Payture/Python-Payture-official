from . import transaction
from . import constants

class TransactionInPay(transaction.Transaction):
    """Transaction class for PaytureInPay"""
    def __init__(self, command, merchant):
        return super(TransactionInPay, self).__init__(constants.PaytureAPIType.apim, command, merchant)
    
    def expandInit(self, data):
        """Expand transaction for EWallet Methods: Init

        Keyword parameters:
        data -- Data object. SessionType and IP are required Url, TemplateTag and Language are optional

        Return value:
        Returns current expanded transaction

        """
        if ( data == None ):
            return self
        self._sessionType = constants.SessionType.Pay
        self._requestKeyValuePair[constants.PaytureParams.Data]  = data._getPropertiesString()
        self._expandMerchant()
        self._expanded = True
        return self
    
    def expandSessionId(self, sessionId):
        """Expand transaction for InPay  Methods: Pay

        Keyword parameters:
        sessionId -- Payment's identifier from Init response

        Return value:
        Returns current expanded transaction

        """
        if (sessionId == None):
            return self
        self._requestKeyValuePair[constants.PaytureParams.SessionId] =  sessionId
        self._expanded = True
        return self

