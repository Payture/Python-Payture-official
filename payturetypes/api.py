from . import transaction
from collections import *
from . import constants

class TransactionAPI(transaction.Transaction):
   """Transaction class for PaytureAPI"""

   def __init__(self, command, merchant):
       super(TransactionAPI, self).__init__(constants.PaytureAPIType.api, command, merchant)
   
   def expandPayBlock(self, info, customFields, customerKey, paytureId):
        """Expand transaction for API Methods: Pay/Block

        Keyword parameters:
        info -- Object that contains params for transaction's processing
        customFields -- Addition fields for processing operation
        customerKey -- Customer's identifier in Payture AntiFraud system
        paytureId -- Payment's identifier in Payture AntiFraud system

        Return value:
        Current expanded transaction

        """
        if(info == None):
            return self
        self._requestKeyValuePair[constants.PaytureParams.PayInfo] =  info._getPropertiesString()
        self._requestKeyValuePair[constants.PaytureParams.OrderId] = info.OrderId
        self._requestKeyValuePair[constants.PaytureParams.Amount] =  info.Amount
        if(customFields != None and len(customFields) != 0):
            self._requestKeyValuePair[constants.PaytureParams.CustomFields] = ''# customFields.Aggregate( "", ( a, c ) => a += $"{c.Key}={c.Value};" ) );

        if (customerKey != None):
            self._requestKeyValuePair[constants.PaytureParams.CustomerKey] = customerKey

        if (paytureId != None):
            self._requestKeyValuePair[constants.PaytureParams.PaytureId] =  paytureId
        self._expandMerchant()
        self._expanded = True
        return self

   def expand3DS(self,  orderId,  paRes):
        """Expand transaction for 3DS Methods: Pay3DS/Block3DS

        Keyword parameters:
        orderId -- Current transaction's identifier in Merchant system
        paRes -- Encrypted string that contains 3DS authentication result (recieved from ACS)

        Return value:
        Current expanded transaction

        """
        self._requestKeyValuePair.Add( constants.PaytureParams.OrderId, orderId )
        self._requestKeyValuePair.Add( constants.PaytureParams.PaRes, paRes )
        self._expandMerchant()
        self._expanded = True
        return self

