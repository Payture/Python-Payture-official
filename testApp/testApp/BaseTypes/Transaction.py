from RequestClient import *
from Constants import *
import string
from PaytureResponse import *
import urllib.parse

class Transaction(RequestClient):
    """Base class for transaction. Contains common fields used in request to Payture server, and common methods - available for all api type"""

    def __init__(self, api, command, merchant):
        self._apiType = api
        self._sessionType = SessionType.Unknown
        self._merchant = merchant
        self._expanded = False
        self.Command = command
        self._requestKeyValuePair = {}
        
    def expand(self, orderId, amount):
        """Expand transaction 

        for API Methods: Charge/UnBlock/Refund/GetState  
        for Ewallet and InPay Methods: Charge/UnBlock/Refund/PayStatus

        Keyword parameters:
        orderId -- Payment's identifier in Merchant system
        amount -- Payment's amount in kopec. Pass null for PayStatus and GetState commands

        Return value:
        Returns current expanded transaction

        """
        if(self._expanded):
            return self
        if(orderId == ''):
            return self

        if(self._apiType == PaytureAPIType.vwapi):
            if(self.Command == PaytureCommands.PayStatus):
                self._requestKeyValuePair[PaytureParams.DATA] = '%s=%s;'%(PaytureParams.OrderId, orderId)
            elif(self.Command == PaytureCommands.Refund and amount != None):
                self._requestKeyValuePair[PaytureParams.DATA] = '%s=%s;%s=%s;%s=%s;'%(PaytureParams.OrderId, orderId, PaytureParams.Amount, amount, PaytureParams.Password, self._merchant.Password)
            elif(amount != None):
                self._requestKeyValuePair[PaytureParams.Amount] = amount
            else:
                self._requestKeyValuePair[PaytureParams.OrderId] = orderId
        else:
            self._requestKeyValuePair[PaytureParams.OrderId] = orderId
            if(amount != None):
                self._requestKeyValuePair[PaytureParams.Amount] = amount

        if(self.Command == PaytureCommands.Refund or (self._apiType != PaytureAPIType.api and (self.Command == PaytureCommands.Charge or self.Command == PaytureCommands.Unblock))):
            self.expandMerchant(True, True)
        else:
            self.expandMerchant()

        self._expanded = True
        return self

    def expandMerchant(self, addKey = True, addPass = False ):
        """ Expand transaction with Merchant key and password

        Keyword parameters:
        addKey -- pass False if Merchant key IS NOT NEEDED
        addPass -- pass true if Merchant password IS NEEDED

        Return value:
        Returns current expanded transaction

        """
        if(addKey):
            self._requestKeyValuePair[(PaytureParams.VWID if self._apiType == PaytureAPIType.vwapi else  PaytureParams.Key)] = self._merchant.MerchantName
        if(addPass):
            self._requestKeyValuePair[PaytureParams.Password] = self._merchant.Password
        return self


    def processAsync(self):
        if(self._expanded == False):
            return PaytureResponse.PaytureResponse.errorResponse(self.Command, 'Params are not set')
        return self.post(self.getPath(),self._requestKeyValuePair) 

    def processSync(self):
        """ Process request to Payture server synchronously

        Return value:
        PaytureResponse - response from the Payture server. In case of exeption will be return PaytureResponse with exeption mesage in ErrCode field.

        """
        if(self._expanded == False):
            return PaytureResponse.PaytureResponse.errorResponse(self.Command, 'Params are not set')
        return self.post(self.getPath(),self._requestKeyValuePair) 

    def getPath(self):
        """Form URL as string for request"""
        return '%s/%s/%s' % (self._merchant.HOST, self._apiType, self.Command)
    
    def formRedirectURL(self, response):
        """  Helper method for PaytureCommand.Init for form Redirect URL and save it in RedirectURL field for convinience"""
        sessionId = response.Attribute[PaytureParams.SessionId]
        response.RedirectURL = '%S/%s/%s?SessionId=%s' % (self._merchant.HOST, self._apiType, PaytureCommands.Add if _sessionType == SessionType.Add else PaytureCommands.Pay, sessionId)
        return response
