from transaction import *
from constants import *

class TransactionInPay(Transaction):
    """Transaction class for PaytureInPay"""
    def __init__(self, command, merchant):
        return super().__init__(PaytureAPIType.apim, command, merchant)
    
    def expandInit(self, data):
        """Expand transaction for EWallet Methods: Init

        Keyword parameters:
        data -- Data object. SessionType and IP are required Url, TemplateTag and Language are optional

        Return value:
        Returns current expanded transaction

        """
        if ( data == None ):
            return self
        self._sessionType = SessionType.Pay
        self._requestKeyValuePair[PaytureParams.Data]  = data.getPropertiesString()
        self.expandMerchant()
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
        self._requestKeyValuePair[PaytureParams.SessionId] =  sessionId
        self._expanded = True
        return self

