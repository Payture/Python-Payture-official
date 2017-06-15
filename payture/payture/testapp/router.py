import random
import sys
import webbrowser
from payture import *

class Router(object):
    def __init__(self, merchant):
        self.Merch = merchant
        self.allFields = {
	                        PaytureParams.VWUserLgn : "testCustomer@test.com",
	                        PaytureParams.VWUserPsw : "pass123",
	                        PaytureParams.CardId : "",
	                        PaytureParams.IP : "12,.0.0.1",
	                        PaytureParams.Amount : "100",
	                        PaytureParams.SessionId : "",
	                        PaytureParams.EMonth : "10",
	                        PaytureParams.EYear : "21",
	                        PaytureParams.CardHolder : "Test Customer",
	                        PaytureParams.SecureCode : "123",
	                        PaytureParams.PhoneNumber : "845693211",
	                        PaytureParams.Email : "testCustomer@test.com",
	                        PaytureParams.OrderId : "",
	                        PaytureParams.SessionType : SessionType.Unknown,
	                        PaytureParams.PAN : "4111111111111112",
	                        PaytureParams.CustomerKey : "testCustomer",
	                        PaytureParams.PaytureId : "",
	                        PaytureParams.CustomFields : "",
	                        PaytureParams.Description : "",
	                        PaytureParams.PaRes : "",
	                        PaytureParams.MD : "",
	                        PaytureParams.PayToken : "",
	                        PaytureParams.Method : "",
	                        PaytureParams.Language : "RU",
	                        PaytureParams.TemplateTag : "",
	                        PaytureParams.Url : "",
	                        PaytureParams.Total : "1",
	                        PaytureParams.Product : "Something"
                        }
        self.rand = random.Random()
        super().__init__()


    def promtapi(self):
        apitype = input("Type the service api type: api, ewallet or inpay: ").lower()
        if(apitype == 'api' or apitype == 'a'):
            return PaytureAPIType.api
        elif(apitype == 'ewallet' or apitype == 'e'):
            return PaytureAPIType.vwapi
        elif(apitype == 'inpay' or apitype == 'i'):
            return PaytureAPIType.apim
        else:
            print ("Illegal service. Only API, EWALLET or INPAY avaliable.")
            return self.promtapi()
        
    def promtsession(self):
        session = input("Specify The Session Type - pay, block or for ewallet only - add: ").lower()
        if(session == 'pay' or session == 'p'):
            return SessionType.Pay
        elif(session == 'block' or session == 'b'):
            return SessionType.Block
        elif(session == 'add' or session == 'a'):
            return SessionType.Add
        else:
            print ("Illegal Session Type. Only pay, block or add avaliable.")
            return self.promtsession()    

    def promtforuseregcard(self):
        reg = input("Use registered card?  Note: type yes/no or y/n: ").lower()
        if(reg == 'yes' or reg == 'y'):
            return True
        elif(reg == 'no' or reg == 'n'):
            return False
        else:
            print ("Illegal input. Type yes/no or y/n for specify necessity of using registered card.")
            return self.promtforuseregcard()   

    def promtforusesessionid(self,command):
        usesessionid = input("Use SessionId for %s command?  Note: type yes/no or y/n: " % (command)).lower()
        if(usesessionid == 'yes' or usesessionid == 'y'):
            return True
        elif(usesessionid == 'no' or usesessionid == 'n'):
            return False
        else:
            print ("Illegal input. Type yes/no or y/n for specify necessity of using SessionId in %s operation." % (command))
            return self.promtforusesessionid(command)   


    def router(self):
        cmd = input("Type the command: ").upper()
        apiType = PaytureAPIType.api
        if(cmd =='PAY'):
            self.pay()
        elif(cmd =='BLOCK'):
            self.block()
        elif(cmd == 'INIT'):
            self.init()
        elif(cmd == 'CHARGE'):
            self.chargeUnblockRefundGetState(PaytureCommands.Charge)
        elif(cmd == 'REFUND'):
            self.chargeUnblockRefundGetState(PaytureCommands.Refund)
        elif(cmd == 'UNBLOCK'):
            self.chargeUnblockRefundGetState(PaytureCommands.Unblock)
        elif(cmd == 'GETSTATE'):
            self.chargeUnblockRefundGetState(PaytureCommands.GetState)
        elif(cmd == 'PAYSTATUS'):
            self.chargeUnblockRefundGetState(PaytureCommands.PayStatus)
        elif(cmd == 'ACTIVATE'):
            self.customerAndCardApi(PaytureCommands.Activate)
        elif(cmd == 'REMOVE'):
            self.customerAndCardApi(PaytureCommands.Remove)
        elif(cmd == 'GETLIST'):
            self.customerAndCardApi(PaytureCommands.GetList)
        elif(cmd == 'REGISTER'):
            self.customerAndCardApi(PaytureCommands.Register)
        elif(cmd == 'UPDATE'):
            self.customerAndCardApi(PaytureCommands.Update)
        elif(cmd == 'DELETE'):
            self.customerAndCardApi(PaytureCommands.Delete)
        elif(cmd == 'CHECK'):
            self.customerAndCardApi(PaytureCommands.Check)
        elif(cmd == 'ADD'):
            if(self.promtforusesessionid(PaytureCommands.Add)):
                self.payturePayOrAdd(PaytureCommands.Add)
                return
            #EWallet add card on Merchant side
            customer = self.getCustomer()
            card = self.getCard()
            self.response = self.Merch.ewallet( PaytureCommands.Add ).expandForMerchantAdd(customer, card).processSync() 
        elif(cmd == 'FIELDS'):
            for key in self.allFields:
                print ('%s = %s' % (key, self.allFields[key]))
            return
        elif(cmd == 'CHANGEFIELDS'):
            self.circleChanges("Change defaults")
        elif(cmd == 'COMMANDS'):
            self.listCommands()
        elif(cmd == 'CHANGEMERCHANT'):
            self.changeMerchant()
        elif(cmd == 'HELP'):
            self.help()
        if(cmd != 'FIELDS' and cmd != 'CHANGEFIELDS' and cmd != 'COMMANDS' and cmd != 'CHANGEMERCHANT' and cmd != 'HELP'):
            self.writeResult()


    def pay(self):
        apitype = self.promtapi()
        if(apitype == PaytureAPIType.api):
            self.apiPayOrBlock(PaytureCommands.Pay)
        elif(promtForUseSessionId(PaytureCommands.Pay)):
            self.payturePayOrAdd(PaytureCommands.Pay)
        elif(apitype == PaytureAPIType.apim):
            print ("PaytureCommands.Pay for PaytureInPay can be process only with SessionId payment's identifier after PaytureCommands.Init api method.\nCall Init and set SessionId parameter.")                        
        else: #only ewallet here
            customer = self.getCustomer()
            data = self.getData(promtsession())
            regcard = self.promtforuseregcard()
            if(regcard == False):
                card = self.getCard()
                self.response = self.Merch.ewallet( PaytureCommands.Pay ).expandForMerchantPayNoReg( customer, card, data ).processSync()
        
            cardId = self.allFields[ PaytureParams.CardId ]
            secureCode = self.allFields[ PaytureParams.SecureCode ]
            print ( "CardId=%s; SecureCode=%s;" % (cardId, secureCode) )
            self.circleChanges( "CardId and SecureCode" )
            self.response = self.Merch.ewallet( PaytureCommands.Pay ).expandForMerchantPayReg(customer,  self.allFields[ PaytureParams.CardId ],  self.allFields[ PaytureParams.SecureCode ],  data).processSync()   
        return


    def block(self):
        self.apiPayOrBlock(PaytureCommands.Block)
        return

    def apiPayOrBlock(self, command):
        payInfo = self.getPayInfo();
        paytureId = self.allFields[PaytureParams.PaytureId]
        custKey = self.allFields[PaytureParams.CustomerKey]
        custFields = self.allFields[PaytureParams.CustomFields]
        props = dir(payInfo)
        propsPayInfo = '' 
        for elem in props:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            propsPayInfo += elem + '=' + str(getattr(payInfo, elem)) + ';\n'
        print( "Additional settings for request:" )
        print( "%s\nPaytureId = %s\nCustomerKey = %s\nCustomFields = %s\n " % (propsPayInfo, paytureId, custKey, custFields) )
        self.circleChanges("Change defaults for pay/block")
        self.response = self.Merch.api(command).expandPayBlock( payInfo, None, self.allFields[PaytureParams.CustomerKey], self.allFields[PaytureParams.PaytureId] ).processSync()
        return
 
    def chargeUnblockRefundGetState(self, command):
        apitype = self.promtapi()
        orderId = self.allFields[PaytureParams.OrderId]
        amount = self.allFields[ PaytureParams.Amount ]
        self.circleChanges("Change defaults")

        if ( apitype == PaytureAPIType.api ):
            self.response = self.Merch.api( command ).expand( orderId,  amount ).processSync()
        elif ( apitype == PaytureAPIType.vwapi ):
            self.response = self.Merch.ewallet( command ).expand( orderId,  amount ).processSync()
        # elif()
        else:
            self.response = self.Merch.inpay( command ).expand( orderId,  amount ).processSync()

    def payturePayOrAdd(self, command):
        sessionId = self.allFields[PaytureParams.SessionId]
        print( 'SessionId: %s' % (sessionId))
        self.circleChanges( "SessionId" )
        self.response = self.Merch.ewallet(command).expandSessionId( self.allFields[PaytureParams.SessionId]).processSync()

    def getCustomer(self):
        customer = self.customerFromCurrentSettings()
        props = dir(customer)
        propsDataDefault = '' 
        for elem in props:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            propsDataDefault += elem + '=' + str(getattr(customer, elem)) + ';\n'
        print( "Default settings for Customer:" )
        print( propsDataDefault )
        self.circleChanges( "Customers fields" )
        return self.customerFromCurrentSettings()

    def customerFromCurrentSettings(self):
        return Customer( self.allFields[ PaytureParams.VWUserLgn ], self.allFields[ PaytureParams.VWUserPsw ], self.allFields[ PaytureParams.PhoneNumber ], self.allFields[ PaytureParams.Email ] )
        


    def getData(self, sessionType):
        self.generateAmount()
        self.generateOrderId()
        self.allFields[ PaytureParams.SessionType ] = sessionType
        data = self.dataFromCurrentSettings()
        props = dir(data)
        propsDataDefault = '' 
        for elem in props:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            propsDataDefault += elem + '=' + str(getattr(data, elem)) + ';\n'
        print( "Default settings for request:" )
        print( propsDataDefault )
        self.circleChanges("Change Data settings")
        return self.dataFromCurrentSettings()

    def dataFromCurrentSettings(self):
        #self.allFields[ PaytureParams.Total ] = self.allFields[ PaytureParams.Amount ]
        return  Data(self.allFields[ PaytureParams.SessionType ],self.allFields[ PaytureParams.IP ], 
                    Amount = self.allFields[ PaytureParams.Amount ],
                    Language = self.allFields[ PaytureParams.Language ],
                    OrderId = self.allFields[ PaytureParams.OrderId ],
                    TemplateTag = self.allFields[ PaytureParams.TemplateTag ],
                    Total = self.allFields[ PaytureParams.Total ],
                    Product = self.allFields[ PaytureParams.Product ])


    def getCard(self):
        card = self.cardFromCurrentSettings()
        props = dir(card)
        propsDataDefault = '' 
        for elem in props:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            propsDataDefault += elem + '=' + str(getattr(card, elem)) + ';\n'
        print( "Default settings for Card:" )
        print( propsDataDefault )
        self.circleChanges("Change Card's settings")
        return self.cardFromCurrentSettings()

    def cardFromCurrentSettings(self):
        return Card( self.allFields[ PaytureParams.PAN ], self.allFields[ PaytureParams.EMonth ],
                   self.allFields[ PaytureParams.EYear ], self.allFields[ PaytureParams.CardHolder ], self.allFields[ PaytureParams.SecureCode ] )

    def getPayInfo(self):
        self.generateAmount();
        self.generateOrderId();
        payInfo = self.payInfoFromCurrentSettings()
        props = dir(payInfo)
        propsPayInfo = '' 
        for elem in props:
            if(elem.startswith('_') or elem.endswith('_') or elem.startswith('get')):
                continue
            propsPayInfo += elem + '=' + str(getattr(payInfo, elem)) + ';\n'
        print( "Default settings PayInfo:" )
        print( propsPayInfo )
        self.circleChanges("Change PayInfo")
        return self.payInfoFromCurrentSettings()

    def payInfoFromCurrentSettings(self):
        return  PayInfo( self.allFields[ PaytureParams.PAN ],
                         self.allFields[ PaytureParams.EMonth ],
                         self.allFields[ PaytureParams.EYear ],
                         self.allFields[ PaytureParams.CardHolder ],
                         self.allFields[ PaytureParams.SecureCode ],
                         self.allFields[ PaytureParams.OrderId ],
                         self.allFields[ PaytureParams.Amount ] )


    def init(self):
        apitype = self.promtapi()
        session = self.promtsession()
        data = self.getData(session)
        if(apitype == PaytureAPIType.vwapi):
            customer = self.getCustomer()
            cardId = self.allFields[ PaytureParams.CardId ]
            self.response = self.Merch.ewallet( PaytureCommands.Init ).expandInit( customer, cardId, data ).processSync()
        else:
            self.response = self.Merch.inpay( PaytureCommands.Init ).expandInit( data ).processSync()
        webbrowser.open(self.response.RedirectURL)

    def customerAndCardApi(self, command):
        customer = self.getCustomer()
        if ( command == PaytureCommands.Activate or command == PaytureCommands.Remove ):
            cardId = self.allFields[ PaytureParams.CardId ]
            print( "CardId: %s" % (cardId) )
            self.circleChanges( "CardId" )
            self.response = self.Merch.ewallet( command ).expandForCardOperation( customer, self.allFields[ PaytureParams.CardId ], 101 if command == PaytureCommands.Activate else None ).processSync()
        self.response = self.Merch.ewallet( command ).expandCustomer( customer ).processSync()

    def circleChanges(self, message):
        val = input("Please enter <1> if you wanna change %s:" % (message))
        if(val == '1'):
            while ( True ):
                if (  input("Type 'end' if you completed changes") == 'end' ):
                    break;  
                self.changeFields()


    def changeFields(self):
        line = input("Enter your params in line separated by space (like this key1=val1 key2=val2): ")
        if ( line == '' ):
            return
        pairs = line.split()
        for pair in pairs:
            keyval = pair.split('=')
            for key in self.allFields:
                if(key.upper() == keyval[0].upper()):
                    self.allFields[key] = keyval[1]

        for key in self.allFields:
            print (key + '=' + self.allFields[key])


    def listCommands(self):
        commands = open("testapp/commandslist.txt", "r")
        print (commands.read())
        commands.close()

    def changeMerchant(self):
        _merchantKey = input('Type Merchant account name: ')
        _merchantPassword = input('Type Merchant account password: ')
        _host = input('Type host name: ')
        print( "Merchant account settings: \n\tMerchantName=%s\n\tMerchantPassword=%s\n\tHOST=%s\n" % (_merchantKey, _merchantPassword, _host) )
        self.Merch = Merchant( _merchantKey, _merchantPassword, _host )

    def help(self):
        help = open("testapp/help.txt", "r")
        print (help.read())
        help.close()
        

    def writeResult(self):
        if(self.response != None):
            print (self.response)


    def generateOrderId(self):
        self.allFields[ PaytureParams.OrderId ] = "ORD_%s_TEST" % (self.rand.randint( 0, 1000000000 ))

    def generateAmount(self):
        self.allFields[ PaytureParams.Amount ] = self.rand.randint( 50, 100000 )
        #self.allFields[ PaytureParams.Amount ] = '%s' % ( self.rand.randint( 50, 100000 ))
