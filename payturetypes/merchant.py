from . import api
from . import digitalwallet
from . import ewallet
from . import inpay
from . import constants


class Merchant(object):
    """Object that contain Merchant account data (login and password) and string value of HOST for requests"""
    
    def __init__(self, accountName, password, host):
        self.MerchantName = accountName
        self.Password = password
        self.HOST = host
        super(Merchant, self).__init__()

    def api(self, command):
        """Create an empty transation for PaytureAPI."""
        return api.TransactionAPI(command, self)
    
    def inpay(self, command):
        """Create an empty transation for PaytureInPay."""
        return inpay.TransactionInPay(command, self)
    
    def ewallet(self, command):
        """Create an empty transation for PaytureEWallet."""
        return ewallet.TransactionEWallet(command, self)
    
    def apple(self, command):
        """Create an empty transation for Payture Apple Pay."""
        return digitalwallet.TransactionDigitalWallet(command, self, constants.PaytureCommands.ApplePay)
    
    def android(self, command):
        """Create an empty transation for Payture Android Pay."""
        return digitalwallet.TransactionDigitalWallet(command, self, constants.PaytureCommands.AndroidPay)
