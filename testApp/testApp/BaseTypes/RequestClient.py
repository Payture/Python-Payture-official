import xml.etree.ElementTree as ET
from PaytureResponse import *
from Constants import *
import requests

class RequestClient(object):
    def __init__(self):
        self.httpClient = None

    def post(self, url, content):
        headers = {"Content-type": "application/x-www-form-urlencoded",
				    "Accept": "text/plain"}
	    #conn = http.client.HTTPConnection(url)
	    #conn.request("POST", url, content, headers)
	    #response = conn.getresponse()
	    #data = response.read()
        r = requests.post(url, content)
        cont = r.content
        print( "Response:\n" + r.text )
        return self.parseXMLResponse(r.text)


	# <summary>
	# Helper method for parsing received response (that in XML format)
	# </summary>
	# <param name="body">String representation of response body</param>
	# <param name="command"></param>
	# <returns>response object</returns>
    def parseXMLResponse(self, responseBody):
        root = ET.fromstring(responseBody)
        print (root.attrib)
        print ('\n\n\n===================================')
        for child in root:
            print(child.tag, child.attrib)
        print ('===================================\n\n\n')
        apiname = root.tag
        err = True  #root.attrib['ErrCode']
        success = root.attrib['Success']
        red = None
        if(apiname == 'Init'):
            red = '%s/%s/%s?%s=%s' % (self._merchant.HOST, self._apiType, self._sessionType, PaytureParams.SessionId, root.attrib[PaytureParams.SessionId] )
        paytureResponse = PaytureResponse(apiname, success, err, RedirectURL = red )
        return paytureResponse

