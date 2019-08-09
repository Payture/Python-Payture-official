from . import transaction
from . import constants

class TransactionEWallet(transaction.Transaction):
    """Transaction class for PaytureEWallet"""
    def __init__(self, command, merchant):
         super(TransactionEWallet, self).__init__(constants.PaytureAPIType.vwapi, command, merchant)
    
    def expandForMerchantAdd(self, customer, card):
        """Expand transaction for EWallet Methods: Add (on Merchant side)

        Keyword parameters:
        customer - Customer object in wich you must specify login and password
        card - Card object with all fields exclude CardId

        Return value:
        Returns current expanded transaction

        """
        if(customer == None or card == None):
            return self
        str = customer._getPropertiesString() + card._getPropertiesString()
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandForMerchantPayNoReg(self, customer, card, data):
        """Expand transaction for EWallet Methods: Pay (Merchant side for NOT REGISTERED card)

        Keyword parameters:
        customer -- Customer object
        card -- Card object. Specify in it all fields exclude CardId
        data -- Data object. SessionType and IP fields are required. Optional ConfimCode and CustomFields

        Return value:
        Returns current expanded transaction

        """
        if(customer == None or card == None or data == None):
            return self
        self._sessionType = data.SessionType
        card.CardId = 'FreePay'
        str = customer._getPropertiesString() + card._getPropertiesString() + data._getPropertiesString() + data.CustomFields
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandForMerchantPayReg(self, customer, cardId, secureCode, data):
        """Expand transaction for EWallet Methods: Pay (Merchant side for REGISTERED card) 

        Keyword parameters:
        customer -- Customer object
        cardId -- CardId identifier in Payture system
        secureCode -- CVC2/CVV2
        data -- Data object. SessionType and IP fields are required. Optional  ConfimCode and CustomFields

        Return value:
        Returns current expanded transaction

        """
        if(customer == None or cardId == None):
            return self
        self._sessionType = data.SesstionType
        str = customer._getPropertiesString() + '%s=%s;' % (PaytureParams.CardId, cardId) + '%s=%s;' % (PaytureParams.SecureCode, secureCode) +  data._getPropertiesString()  + data.CustomFields;
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandCustomer(self, customer):
        """Expand transaction for EWallet Methods: Register/Update/Delete/Check/Getlist 

        Keyword parameters:
        customer -- Customer object in wich you must specify login and password; all remaining fields is optional

        Return value:
        Returns current expanded transaction

        """
        str = ''
        if(self.Command == constants.PaytureCommands.Delete):
            str +=  '%s=%s;%s=%s;' % (constants.PaytureParams.VWUserLgn, customer.VWUserLgn, constants.PaytureParams.Password, self._merchant.Password)
        else:
            str += customer._getPropertiesString()
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandInit(self, customer, cardId, data):
        """Expand transaction for EWallet Methods: Init

        Keyword parameters:
        customer -- Customer object
        cardId -- CardId identifier in Payture system
        data -- Data object. SessionType and IP fields are required; Optional TamplateTag and Language

        Return value:
        Returns current expanded transaction

        """

        if(customer == None or data == None):
            return self
        self._sessionType = data.SessionType
        str = customer._getPropertiesString() + ( '' if cardId == None else 'CardId=%s;' %(cardId) ) + data._getPropertiesString() + ( data.CustomFields if hasattr(data, 'CustomFields') else '');
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandForCardOperation(self, customer, cardId, amount, orderId = None):
        """Expand transaction for EWallet Methods: SendCode/Activate/Remove

        Keyword parameters:
        customer -- Customer object in which you must specify login and password fields
        cardId -- Cards identifier in Payture system
        amount -- Payment's identifier in Merchant system. For Remove pass null
        orderId -- Payment's amount in kopec. For Activate and Remove pass null

        Return value:
        Returns current expanded transaction

        """
        if(customer == None or cardId == None):
            return self
        str = customer._getPropertiesString() + '%s=%s;' %(constants.PaytureParams.CardId, cardId) + ( '%s=%s;' % (constants.PaytureParams.Amount, amount) if amount != None and self.Command == constants.PaytureCommands.Activate else '' ) + ( '' if orderId == None else '%s=%s;'%(constants.PaytureParams.OrderId, orderId) )
        return self._expandInternal(constants.PaytureParams.DATA, str)
    
    def expandSessionId(self, sessionId):
        """Expand transaction for EWallet  Methods: Pay/Add (on Payture side)

        Keyword parameters:
        sessionId -- Payment's identifier from Init response

        Return value:
        Returns current expanded transaction

        """
        if(sessionId == None):
            return self
        self._requestKeyValuePair[constants.PaytureParams.SessionId] =  sessionId 
        self._expanded = True
        return self
    
    def expandPaySubmit3DS(self, md, pares):
        """Expand transaction for PaySubmit3DS

        Keyword parameters:
        MD -- Unique transaction identifier from ACS response
	    paRes -- An encrypted string with the result of 3DS Authentication

        Return value:
        Returns current expanded transaction

        """
        self._requestKeyValuePair[constants.PaytureParams.MD] = md
        self._requestKeyValuePair[constants.PaytureParams.PaRes] = pares
        self._expanded = True
        return self
    
    def _expandInternal(self, field, data):
        self._requestKeyValuePair[field] = data
        self._expandMerchant()
        self._expanded = True
        return self
