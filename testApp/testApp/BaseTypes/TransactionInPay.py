from Transaction import *
from Constants import *

class TransactionInPay(Transaction):

	def __init__(self, command, merchant):
		return super().__init__(PaytureAPIType.apim, command, merchant)

	# <summary>
	# Expand transaction for InPay Methods: Init
	# </summary>
	# <param name="data">Data object. SessionType and IP are required Url, TemplateTag and Language are optional.</param>
	# <returns>current expanded transaction</returns>
	def expandInit(self, data):
		if ( data == None ):
			return self
		self._sessionType = SessionType.Pay
		self._requestKeyValuePair[PaytureParams.Data]  = data.getPropertiesString()
		self.expandMerchant()
		self._expanded = True
		return self


	# <summary>
	# Expand transaction for InPay  Methods: Pay
	# </summary>
	# <param name="sessionId">Payment's identifier from Init response.</param>
	# <returns>current expanded transaction</returns>
	def expandSessionId(self, sessionId):
		if (sessionId == None):
			return self
		self._requestKeyValuePair[PaytureParams.SessionId] =  sessionId
		self._expanded = True
		return self

