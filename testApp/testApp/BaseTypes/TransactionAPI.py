from Transaction import *
from collections import *

class TransactionAPI(Transaction):
   
	def __init__(self, command, merchant): 
		return super().__init__(PaytureAPIType.api, command, merchant)

    # <summary>
    # Expand transaction for API Methods: Pay/Block
    # </summary>
    # <param name="info"></param>
    # <param name="customFields"></param>
    # <param name="customerKey"></param>
    # <param name="paytureId"></param>
    # <returns>current expanded transaction</returns>
	def expandPayBlock(self, info, customFields, customerKey, paytureId):
		if(info == None):
			return self
		self._requestKeyValuePair[PaytureParams.PayInfo] =  info.getPropertiesString()
		self._requestKeyValuePair[PaytureParams.OrderId] = info.OrderId
		self._requestKeyValuePair[PaytureParams.Amount] =  info.Amount
		if(customFields != None and len(customFields) != 0):
			self._requestKeyValuePair[PaytureParams.CustomFields] = ''# customFields.Aggregate( "", ( a, c ) => a += $"{c.Key}={c.Value};" ) );

		if (customerKey != None):
			self._requestKeyValuePair[PaytureParams.CustomerKey] = customerKey

		if (paytureId != None):
			self._requestKeyValuePair[PaytureParams.PaytureId] =  paytureId

		self.expandMerchant()
		self._expanded = True;
		return self



        # <summary>
        # Expand transaction for 3DS Methods: Pay3DS/Block3DS
        # </summary>
        # <param name="orderId"></param>
        # <param name="paRes"></param>
        # <returns>current expanded transaction</returns>
	def expand3DS(self,  orderId,  paRes):
		self._requestKeyValuePair.Add( PaytureParams.OrderId, orderId )
		self._requestKeyValuePair.Add( PaytureParams.PaRes, paRes )
		self.expandMerchant()
		self._expanded = True
		return self;
