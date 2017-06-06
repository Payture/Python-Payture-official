from Transaction import *

class TransactionEWallet(Transaction):
	def __init__(self, command, merchant):
		return super().__init__(PaytureAPIType.vwapi, command, merchant)

	# <summary>
    # Expand transaction for EWallet Methods: Add (on Merchant side)
    # </summary>
    # <param name="customer">Customer object in wich you must specify login and password.</param>
    # <param name="card">Card card with all fields exclude CardId.</param>
    # <returns>current expanded transaction</returns>
	def expandForMerchantAdd(self, customer, card):
		if(customer == None or card == None):
			return self
		str = customer.getPropertiesString() + card.getPropertiesString()
		return self.expandInternal(PaytureParams.DATA, str)



	# <summary>
    # Expand transaction for EWallet Methods: Pay (Merchant side for NOT REGISTERED card)
    # </summary>
    # <param name="customer">Customer object.</param>
    # <param name="card">Card object. Specify in it all fields exclude CardId.</param>
    # <param name="data">Data object. SessionType and IP fields are required. Optional ConfimCode and CustomFields.</param>
    # <returns>current expanded transaction</returns>
	def expandForMerchantPayReg(self, customer, card, data):
		if(customer == None or card == None or data == None):
			return self
		self._sessionType = data.SessionType
		card.CardId = 'FreePay'
		str = customer.getPropertiesString() + card.getPropertiesString() + data.getPropertiesString() + data.CustomFields
		return self.expandInternal(PaytureParams.DATA, str)



	# <summary>
    # Expand transaction for EWallet Methods: Pay (Merchant side for REGISTERED card) 
    # </summary>
    # <param name="customer">Customer object.</param>
    # <param name="cardId">CardId identifier in Payture system.</param>
    # <param name="secureCode">CVC2/CVV2.</param>
    # <param name="data">Data object. SessionType and IP fields are required. Optional  ConfimCode and CustomFields.</param>
    # <returns>current expanded transaction</returns>
	def expandForMerchantPayNoReg(self, customer, cardId, secureCode, data):
		if(customer == None or cardId == None):
			return self
		self._sessionType = data.SesstionType
		str = customer.getPropertiesString() + '%s=%s;' % (PaytureParams.CardId, cardId) + '%s=%s;' % (PaytureParams.SecureCode, secureCode) +  data.getPropertiesString()  + data.CustomFields;
		return self.expandInternal(PaytureParams.DATA, str)

	# <summary>
    # Expand transaction for EWallet Methods: Register/Update/Delete/Check/Getlist 
    # </summary>
    # <param name="customer">Customer object in wich you must specify login and password; all remaining fields is optional.</param>
    # <returns>current expanded transaction</returns>
	def expandCustomer(self, customer):
		str = ''
		if(self.Command == PaytureCommands.Delete):
			str +=  '%s=%s;%s=%s;' % (PaytureParams.VWUserLgn, customer.VWUserLgn, PaytureParams.Password, self._merchant.Password)
		else:
			str += customer.getPropertiesString()
		return self.expandInternal(PaytureParams.DATA, str)

	# <summary>
    # Expand transaction for EWallet Methods: Init
    # </summary>
    # <param name="customer">Customer object.</param>
    # <param name="cardId">CardId identifier in Payture system.</param>
    # <param name="data">Data object. SessionType and IP fields are required; Optional TamplateTag and Language.</param>
    # <returns>current expanded transaction</returns>
	def expandInit(self, customer, cardId, data):
		if(customer == None or data == None):
			return self
		self._sessionType = data.SessionType
		str = customer.getPropertiesString() + ( '' if cardId == None else 'CardId=%s;' %(cardId) ) + data.getPropertiesString() + ( data.CustomFields if hasattr(data, 'CustomFields') else '');
		return self.expandInternal(PaytureParams.DATA, str)



	# <summary>
    # Expand transaction for EWallet Methods: SendCode/Activate/Remove
    # </summary>
    # <param name="customer">Customer object in which you must specify login and password fields.</param>
    # <param name="cardId">Cards identifier in Payture system.</param>
    # <param name="amount">Payment's identifier in Merchant system. For Remove pass null.</param>
    # <param name="orderId">Payment's amount in kopec. For Activate and Remove pass null.</param>
    # <returns>current expanded transaction</returns>
	def expandForCardOperation(self, customer, cardId, amount, orderId = None):
		if(customer == None or cardId == None):
			return self
		str = customer.getPropertiesString() + '%s=%s;' %(PaytureParams.CardId, cardId) + ( '%s=%s;' % (PaytureParams.Amount, amount) if amount != None and self.Command == PaytureCommands.Activate else '' ) + ( '' if orderId == None else '%s=%s;'%(PaytureParams.OrderId, orderId) )
		return self.expandInternal(PaytureParams.DATA, str)

	# <summary>
	# Expand transaction for EWallet  Methods: Pay/Add (on Payture side)
	# </summary>
	# <param name="sessionId">Payment's identifier from Init response.</param>
	# <returns>current expanded transaction</returns>
	def expandSessionId(self, sessionId):
		if(sessionId == None):
			return self
		self._requestKeyValuePair[PaytureParams.SessionId] =  sessionId 
		self._expanded = True;
		return self


	# <summary>
	# Expand transaction for PaySubmit3DS
	# </summary>
	# <param name="MD">Unique transaction identifier from ACS response.</param>
	# <param name="paRes">An encrypted string with the result of 3DS Authentication.</param>
	# <returns>current expanded transaction</returns>
	def expandPaySubmit3DS(self, md, pares):
		self._requestKeyValuePair[PaytureParams.MD] = md
		self._requestKeyValuePair[PaytureParams.PaRes] = pares
		self._expanded = True;
		return self


	def expandInternal(self, field, data):
		self._requestKeyValuePair[field] = data
		self.expandMerchant()
		self._expanded = True
		return self
