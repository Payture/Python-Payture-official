from CardInfo import *
from Constants import *
from Merchant import *
from PaytureResponse import *
from RequestClient import *
from Transaction import *
from TransactionAPI import *
from TransactionEWallet import *
from TransactionInPay import *
from TransactionDigitalWallet import *
from Card import *
from Customer import *
from Data import *
from EncodeString import *
from PayInfo import *
import string
from router import *

_host = "http://sasha:7080";
_merchantKey = "elena_Test";
_merchantPassword = "789555";


merchant = Merchant(_merchantKey, _merchantPassword, _host)
rout = Router(merchant)

str = input( "Press space for get description of commands for this console program. " )
if(str == ' '):
	rout.help()
	str = input( "Press space for get command's list. " )
	if(str == ' '):
		rout.listCommands()
		str = input( "Press enter for continue. " )

print ( "Merchant account settings: \n\tMerchantName=%s\n\tMerchantPassword=%s\n\tHOST=%s\n" % (_merchantKey, _merchantPassword, _host) );
str = input( "Press space for change Merchant account settings. " )
if(str == ' '):
	rout.changeMerchant()


while(True):
    str = input( "Type 'end' for exit: ")
    if(str == 'end'):
        break
    rout.router()
