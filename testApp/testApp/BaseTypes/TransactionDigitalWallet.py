from Transaction import *

class TransactionDigitalWallet(Transaction):
	
	def __init__(self, command, merchant, spetialCmd):
		self._specialCommand = specialCommand
		return super().__init__(PaytureAPIType.api, command, merchant)


	#<summary>
	#Expand transaction for ApplePay and AndroidPay Methods: Pay/Block
	#</summary>
	#<param name="payToken">PaymentData from PayToken for current transaction.</param>
	#<param name="orderId">Current transaction OrderId.</param>
	#<param name="amount">Current transaction amount in kopec - pass null for Apple Pay.</param>
	#<returns>current expanded transaction</returns>
	def expandPayBlock(self, payToken, orderId, amount):
		self._requestKeyValuePair[PaytureParams.OrderId] = orderId
		self._requestKeyValuePair[PaytureParams.PayToken] =  payToken 
		self._requestKeyValuePair[PaytureParams.Method] = DigitalPayMethods.PAY if  Command == PaytureCommands.Pay else DigitalPayMethods.BLOCK
		self.expand();
		if(self._specialCommand == PaytureCommands.AndroidPay and amount != None):
			self._requestKeyValuePair[PaytureParams.Amount] = amount

		self.Command =  _specialCommand;
		self._expanded = True
		return self
