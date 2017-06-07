from api import *
from digitalwallet import *
from ewallet import *
from inpay import *
from constants import *

class Merchant(object):
    """Object that contain Merchant account data (login and password) and string value of HOST for requests"""
    
    def __init__(self, accountName, password, host):
        self.MerchantName = accountName
        self.Password = password
        self.HOST = host

    def api(self, command):
        """Create an empty transation for PaytureAPI."""
        return TransactionAPI(command, self)
    
    def inpay(self, command):
        """Create an empty transation for PaytureInPay."""
        return TransactionInPay(command, self)
    
    def ewallet(self, command):
        """Create an empty transation for PaytureEWallet."""
        return TransactionEWallet(command, self)
    
    def apple(self, command):
        """Create an empty transation for Payture Apple Pay."""
        return TransactionDigitalWallet(command, self, PaytureCommands.ApplePay)
    
    def android(self, command):
        """Create an empty transation for Payture Android Pay."""
        return TransactionDigitalWallet(command, self, PaytureCommands.AndroidPay)
