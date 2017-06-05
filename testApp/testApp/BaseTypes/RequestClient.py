import xml.etree.ElementTree as ET
from PaytureResponse import *
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
        self.parseXMLResponse(r.text)
        return r


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
        apiname = ''
        err = ''
        success = True
        red = None
        if(apiname == 'Init'):
            red = ''
        paytureResponse = PaytureResponse(apiname, success, err, RedirectURL = red )
        return paytureResponse

