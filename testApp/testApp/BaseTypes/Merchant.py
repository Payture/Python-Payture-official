from TransactionAPI import *
from TransactionDigitalWallet import *
from TransactionEWallet import *
from TransactionInPay import *
from Constants import *

class Merchant(object):
	
	def __init__(self, accountName, password, host):
		self.MerchantName = accountName
		self.Password = password
		self.HOST = host

	def api(self, command):
		return TransactionAPI(command, self)

	def inpay(self, command):
		return TransactionInPay(command, self)

	def ewallet(self, command):
		return TransactionEWallet(command, self)

	def apple(self, command):
		return TransactionDigitalWallet(command, self, PaytureCommands.ApplePay)

	def android(self, command):
		return TransactionDigitalWallet(command, self, PaytureCommands.AndroidPay)
