from transaction import *
from constants import *

class TransactionDigitalWallet(Transaction):
    """Transaction class for Payture ApplePay and Payture AndroidPay"""
    
    def __init__(self, command, merchant, specialcmd):
        self._specialCommand = specialcmd
        super().__init__(PaytureAPIType.api, command, merchant)
    
    def expandPayBlock(self, payToken, orderId, amount):
        """Expand transaction for ApplePay and AndroidPay Methods: Pay/Block

        Keyword parameters:
        payToken -- PaymentData from PayToken for current transaction
	    orderId -- current transaction OrderId
	    amount -- current transaction amount in kopec - pass null for Apple Pay

        Return value:
        Returns current expanded transaction

        """
        self._requestKeyValuePair[PaytureParams.OrderId] = orderId
        self._requestKeyValuePair[PaytureParams.PayToken] =  payToken 
        self._requestKeyValuePair[PaytureParams.Method] = DigitalPayMethods.PAY if  Command == PaytureCommands.Pay else DigitalPayMethods.BLOCK
        self.expandMerchant()
        if(self._specialCommand == PaytureCommands.AndroidPay and amount != None):
            self._requestKeyValuePair[PaytureParams.Amount] = amount
        self.Command =  self._specialCommand
        self._expanded = True
        return self
