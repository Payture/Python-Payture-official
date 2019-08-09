from . import transaction
from . import constants

class TransactionDigitalWallet(transaction.Transaction):
    """Transaction class for Payture ApplePay and Payture AndroidPay"""
    
    def __init__(self, command, merchant, specialcmd):
        self._specialCommand = specialcmd
        super(TransactionDigitalWallet, self).__init__(constants.PaytureAPIType.api, command, merchant)
    
    def expandPayBlock(self, payToken, orderId, amount):
        """Expand transaction for ApplePay and AndroidPay Methods: Pay/Block

        Keyword parameters:
        payToken -- PaymentData from PayToken for current transaction
	    orderId -- current transaction OrderId
	    amount -- current transaction amount in kopec - pass null for Apple Pay

        Return value:
        Returns current expanded transaction

        """
        self._requestKeyValuePair[constants.PaytureParams.OrderId] = orderId
        self._requestKeyValuePair[constants.PaytureParams.PayToken] =  payToken 
        self._requestKeyValuePair[constants.PaytureParams.Method] = constants.DigitalPayMethods.PAY if  Command == constants.PaytureCommands.Pay else constants.DigitalPayMethods.BLOCK
        self._expandMerchant()
        if(self._specialCommand == constants.PaytureCommands.AndroidPay and amount != None):
            self._requestKeyValuePair[constants.PaytureParams.Amount] = amount
        self.Command =  self._specialCommand
        self._expanded = True
        return self
