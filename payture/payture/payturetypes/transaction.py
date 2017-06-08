from . import constants
import requests
import xml.etree.ElementTree as ET
from . import paytureresponse as pr

class RequestClient(object):
    """Base class for posting request to Payture server"""
    def __init__(self):
        super().__init__()

    def post(self, url, content):
        """Sync "POST" HTTP method for pass data to Payture"""
        r = requests.post(url, content)
        cont = r.content
        print( "Response:\n" + r.text )
        return self.parseXMLResponse(r.text)


    def parseXMLResponse(self, responseBody):
        """Helper method for parsing received response (that in XML format) 

        for API Methods: Charge/UnBlock/Refund/GetState  
        for Ewallet and InPay Methods: Charge/UnBlock/Refund/PayStatus

        Keyword parameters:
	    body -- String representation of response body
	    command --

        Return value:
        Return PaytureResponse object

        """

        root = ET.fromstring(responseBody)
        print (root.attrib)
        print ('\n\n\n' + '=' * 30 )
        for child in root:
            print(child.tag, child.attrib)
        print ('=' * 30 + '\n\n\n')
        apiname = root.tag
        err = True  #root.attrib['ErrCode']
        success = root.attrib['Success']
        red = None
        if(apiname == 'Init'):
            red = '%s/%s/%s?%s=%s' % (self._merchant.HOST, self._apiType, self._sessionType, constants.PaytureParams.SessionId, root.attrib[constants.PaytureParams.SessionId] )
        paytureResponse = pr.PaytureResponse(apiname, success, err, RedirectURL = red )
        return paytureResponse


class Transaction(RequestClient):
    """Base class for transaction. Contains common fields used in request to Payture server, and common methods - available for all api type"""

    def __init__(self, api, command, merchant):
        self._apiType = api
        self._sessionType = constants.SessionType.Unknown
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

        if(self._apiType == constants.PaytureAPIType.vwapi):
            if(self.Command == constants.PaytureCommands.PayStatus):
                self._requestKeyValuePair[constants.PaytureParams.DATA] = '%s=%s;'%(constants.PaytureParams.OrderId, orderId)
            elif(self.Command == constants.PaytureCommands.Refund and amount != None):
                self._requestKeyValuePair[constants.PaytureParams.DATA] = '%s=%s;%s=%s;%s=%s;'%(constants.PaytureParams.OrderId, orderId, constants.PaytureParams.Amount, amount, constants.PaytureParams.Password, self._merchant.Password)
            elif(amount != None):
                self._requestKeyValuePair[constants.PaytureParams.Amount] = amount
            else:
                self._requestKeyValuePair[constants.PaytureParams.OrderId] = orderId
        else:
            self._requestKeyValuePair[constants.PaytureParams.OrderId] = orderId
            if(amount != None):
                self._requestKeyValuePair[constants.PaytureParams.Amount] = amount

        if(self.Command == constants.PaytureCommands.Refund or (self._apiType != constants.PaytureAPIType.api and (self.Command == constants.PaytureCommands.Charge or self.Command == constants.PaytureCommands.Unblock))):
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
            self._requestKeyValuePair[(constants.PaytureParams.VWID if self._apiType == constants.PaytureAPIType.vwapi else  constants.PaytureParams.Key)] = self._merchant.MerchantName
        if(addPass):
            self._requestKeyValuePair[constants.PaytureParams.Password] = self._merchant.Password
        return self


    def processAsync(self):
        if(self._expanded == False):
            return PaytureResponse.errorResponse(self.Command, 'Params are not set')
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
        sessionId = response.Attribute[constants.PaytureParams.SessionId]
        response.RedirectURL = '%S/%s/%s?SessionId=%s' % (self._merchant.HOST, self._apiType, constants.PaytureCommands.Add if _sessionType == constants.SessionType.Add else constants.PaytureCommands.Pay, sessionId)
        return response


