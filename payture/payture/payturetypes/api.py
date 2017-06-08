from . import  transaction
from collections import *
from . import constants

class TransactionAPI(transaction.Transaction):
   """Transaction class for PaytureAPI"""

   def __init__(self, command, merchant): 
       return super().__init__(constants.PaytureAPIType.api, command, merchant)
   
   def expandPayBlock(self, info, customFields, customerKey, paytureId):
        """Expand transaction for API Methods: Pay/Block

        Keyword parameters:
        info --
        customFields --
        customerKey --
        paytureId --

        Return value:
        Current expanded transaction

        """
        if(info == None):
            return self
        self._requestKeyValuePair[constants.PaytureParams.PayInfo] =  info.getPropertiesString()
        self._requestKeyValuePair[constants.PaytureParams.OrderId] = info.OrderId
        self._requestKeyValuePair[constants.PaytureParams.Amount] =  info.Amount
        if(customFields != None and len(customFields) != 0):
            self._requestKeyValuePair[constants.PaytureParams.CustomFields] = ''# customFields.Aggregate( "", ( a, c ) => a += $"{c.Key}={c.Value};" ) );

        if (customerKey != None):
            self._requestKeyValuePair[constants.PaytureParams.CustomerKey] = customerKey

        if (paytureId != None):
            self._requestKeyValuePair[constants.PaytureParams.PaytureId] =  paytureId
        self.expandMerchant()
        self._expanded = True
        return self

   def expand3DS(self,  orderId,  paRes):
        """Expand transaction for 3DS Methods: Pay3DS/Block3DS

        Keyword parameters:
        orderId --
        paRes --

        Return value:
        Current expanded transaction

        """
        self._requestKeyValuePair.Add( constants.PaytureParams.OrderId, orderId )
        self._requestKeyValuePair.Add( constants.PaytureParams.PaRes, paRes )
        self.expandMerchant()
        self._expanded = True
        return self

