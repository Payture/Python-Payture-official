import string
import payture
from router import *

_host = "http://sasha:7080";
_merchantKey = "elena_Test";
_merchantPassword = "789555";


merchant = payture.Merchant(_merchantKey, _merchantPassword, _host)
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
    try:
        rout.router()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        str = input("Press Enter for closing app.")
        break;
