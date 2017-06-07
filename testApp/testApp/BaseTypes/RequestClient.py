import xml.etree.ElementTree as ET
from PaytureResponse import *
from Constants import *
import requests

class RequestClient(object):
    """Base class for posting request to Payture server"""
    def __init__(self):
        return super().__init__()

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
            red = '%s/%s/%s?%s=%s' % (self._merchant.HOST, self._apiType, self._sessionType, PaytureParams.SessionId, root.attrib[PaytureParams.SessionId] )
        paytureResponse = PaytureResponse(apiname, success, err, RedirectURL = red )
        return paytureResponse

