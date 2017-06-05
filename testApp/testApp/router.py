import random
import webbrowser
from Constants import *
from Merchant import *
from PayInfo import *
from Card import *
from Customer import *
from Data import *

class Router(object):
    def __init__(self, merchant):
        self.Merchant = merchant
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
	                        PaytureParams.PhoneNumber : ",845693211",
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
        api = input("Type the service api type: api, ewallet or inpay: ").lower()
        if(api == 'api' or api == 'a'):
            return PaytureAPIType.api
        elif(api == 'ewallet' or api == 'e'):
            return PaytureAPIType.vwapi
        elif(api == 'inpay' or api == 'i'):
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
            self.chargeUnblockRefundGetState(PaytureCommands.Charge)
        elif(cmd == 'UNBLOCK'):
            self.chargeUnblockRefundGetState(PaytureCommands.Charge)
        elif(cmd == 'GETSTATE'):
            self.chargeUnblockRefundGetState(PaytureCommands.Charge)
        elif(cmd == 'PAYSTATUS'):
            self.chargeUnblockRefundGetState(PaytureCommands.Charge)
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
            self.response = self.Merchant.ewallet( PaytureCommands.Add ).expandForMerchantAdd(customer, card).processSync() 
        elif(cmd == 'FIELDS'):
            #var aggrStr = allFields.Aggregate( $"\nCurrent value of fields:\n", ( a, c ) => a += $"\t{c.Key} = {c.Value}\n" );
            #print( aggrStr );
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
        api = self.promtapi()
        if(api == PaytureAPIType.api):
            self.apiPayOrBlock(PaytureCommands.Pay)
        elif(promtForUseSessionId(PaytureCommands.Pay)):
            self.payturePayOrAdd(PaytureCommands.Pay)
        elif(api == PaytureAPIType.apim):
            print ("PaytureCommands.Pay for PaytureInPay can be process only with SessionId payment's identifier after PaytureCommands.Init api method.\nCall Init and set SessionId parameter.")                        
        else: #only ewallet here
            customer = self.getCustomer()
            data = self.getData(promtsession())
            regcard = self.promtforuseregcard()
            if(regcard == False):
                card = self.getCard()
                self.response = self.Merchant.ewallet( PaytureCommands.Pay ).expandForMerchantPayNoReg( customer, card, data ).processSync()
        
            cardId = self.allFields[ PaytureParams.CardId ]
            secureCode = self.allFields[ PaytureParams.SecureCode ]
            print ( "CardId=%s; SecureCode=%s;" % (cardId, secureCode) )
            self.circleChanges( "CardId and SecureCode" )
            self.response = self.Merchant.ewallet( PaytureCommands.Pay ).expandForMerchantPayReg(customer,  self.allFields[ PaytureParams.CardId ],  self.allFields[ PaytureParams.SecureCode ],  data).processSync()   
        return


    def block(self):
        self.apiPayOrBlock(PaytureCommands.Block)
        return

    def apiPayOrBlock(self, command):
        payInfo = self.getPayInfo();
        paytureId = self.allFields[PaytureParams.PaytureId];
        custKey = self.allFields[PaytureParams.CustomerKey];
        custFields = self.allFields[PaytureParams.CustomFields];
        propsPayInfo = ''#payInfo.GetType().GetProperties().Aggregate( $"PayInfo params:\n", ( a, c ) => a += $"\t{c.Name} = {c.GetValue( payInfo, null )}\n" )  CHANGE THIS!!
        print( "Additional settings for request:" )
        print( "%s\nPaytureId = %s\nCustomerKey = %s\nCustomFields = %s\n " % (propsPayInfo, paytureId, custKey, custFields) );
        self.circleChanges("Change defaults for pay/block")
        self.response = self.Merchant.api(command).expandPayBlock( payInfo, None, self.allFields[PaytureParams.CustomerKey], self.allFields[PaytureParams.PaytureId] ).processSync()
        return
 
    def chargeUnblockRefundGetState(self, command):
        api = self.promtapi()
        orderId = self.allFields[PaytureParams.OrderId]
        amount = self.allFields[ PaytureParams.Amount ]
        self.circleChanges("Change defaults")

        if ( api == PaytureAPIType.api ):
            self.response = self.Merchant.api( command ).expand( orderId,  amount ).processSync()
        elif ( api == PaytureAPIType.vwapi ):
            self.response = self.Merchant.ewallet( command ).expand( orderId,  amount ).processSync()
        # elif()
        else:
            self.response = self.Merchant.inpay( command ).expand( orderId,  amount ).processSync()

    def payturePayOrAdd(self, command):
        sessionId = self.allFields[PaytureParams.SessionId]
        print( 'SessionId: %s' % (sessionId))
        self.circleChanges( "SessionId" )
        self.response = merchant.ewallet(command).expandSessionId( self.allFields[PaytureParams.SessionId]).processSync()

    def getCustomer(self):
        customer = self.customerFromCurrentSettings()
        propsDataDefault = '' #customer.GetType().GetProperties().Aggregate( $"Data params:\n", ( a, c ) => a += $"\t{c.Name} = {c.GetValue( customer, null )}\n" ); CHANGE THIS!!
        print( "Default settings for Customer:" )
        print('Oooops!')#"{propsDataDefault} " )
        self.circleChanges( "Customers fields" )
        return self.customerFromCurrentSettings()

    def customerFromCurrentSettings(self):
        return Customer( self.allFields[ PaytureParams.VWUserLgn ], self.allFields[ PaytureParams.VWUserPsw ], self.allFields[ PaytureParams.PhoneNumber ], self.allFields[ PaytureParams.Email ] )
        


    def getData(self, sessionType):
        self.generateAmount()
        self.generateOrderId()
        self.allFields[ PaytureParams.SessionType ] = sessionType
        data = self.dataFromCurrentSettings()
        propsDataDefault = '' #data.GetType().GetProperties().Aggregate( $"Data params:\n", ( a, c ) => a += $"\t{c.Name} = {c.GetValue( data, null )}\n" ); CHANGE THIS!
        print( "Default settings for request:" )
        print('Oooops!!')# $@"{propsDataDefault} " );
        self.circleChanges("Change Data settings")
        return self.dataFromCurrentSettings()

    def dataFromCurrentSettings(self):
        self.allFields[ PaytureParams.Total ] = self.allFields[ PaytureParams.Amount ]
        return  Data(Amount = self.allFields[ PaytureParams.Amount ],
                    IP = self.allFields[ PaytureParams.IP ],
                    Language = self.allFields[ PaytureParams.Language ],
                    OrderId = self.allFields[ PaytureParams.OrderId ],
                    SessionType = self.allFields[ PaytureParams.SessionType ],
                    TemplateTag = self.allFields[ PaytureParams.TemplateTag ],
                    Total = self.allFields[ PaytureParams.Amount ],
                    Product = self.allFields[ PaytureParams.Product ])


    def getCard(self):
        card = self.cardFromCurrentSettings()
        propsDataDefault = '' #card.GetType().GetProperties().Aggregate( $"Data params:\n", ( a, c ) => a += $"\t{c.Name} = {c.GetValue( card, null )}\n" ) CHANGE THIS
        print( "Default settings for Card:" )
        print( 'Opps!' ) #$@"{propsDataDefault} " );
        self.circleChanges("Change Card's settings")
        return self.cardFromCurrentSettings()

    def cardFromCurrentSettings(self):
        return Card( self.allFields[ PaytureParams.PAN ], self.allFields[ PaytureParams.EMonth ],
                   self.allFields[ PaytureParams.EYear ], self.allFields[ PaytureParams.CardHolder ], self.allFields[ PaytureParams.SecureCode ] )

    def getPayInfo(self):
        self.generateAmount();
        self.generateOrderId();
        payInfo = self.payInfoFromCurrentSettings();
        propsPayInfo = '' #payInfo.GetType().GetProperties().Aggregate( $"PayInfo params:\n", ( a, c ) => a += $"\t{c.Name} = {c.GetValue( payInfo, null )}\n" ); CHANGE THIS!!
        print( "Default settings PayInfo:" )
        print( 'Oops!' )# $@"{propsPayInfo}\n" )
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
        api = self.promtapi()
        session = self.promtsession()
        data = self.getData(session)
        if(api == PaytureAPIType.vwapi):
            customer = self.getCustomer()
            cardId = self.allFields[ PaytureParams.CardId ]
            self.response = self.Merchant.ewallet( PaytureCommands.Init ).expandInit( customer, cardId, data ).processSync()
        else:
            self.response = self.Merchant.inpay( PaytureCommands.Init ).expandInit( data ).processSync()
        webbrowser.open(self.response.RedirectURL)
        #logic for open browser is needed
        #var res = response;
        #Task.Run(() => Process.Start($"{res.RedirectURL}"));

    def customerAndCardApi(self, command):
        customer = self.getCustomer()
        if ( command == PaytureCommands.Activate or command == PaytureCommands.Remove ):
            cardId = self.allFields[ PaytureParams.CardId ]
            print( "CardId: %s" % (cardId) )
            self.circleChanges( "CardId" )
            self.response = merchant.ewallet( command ).expandForCardOperation( customer, self.allFields[ PaytureParams.CardId ], 101 if command == PaytureCommands.Activate else None ).processSync()
        self.response = merchant.ewallet( command ).expandCustomer( customer ).processSync()

    def circleChanges(self, message):
        val = input("Please enter <1> if you wanna change %s:" % (message))
        if(val == '1'):
            while ( True ):
                if (  input("Type 'end' if you completed changes") == 'end' ):
                    break;  
                self.changeFields()


    def changeFields(self):
        line = input("Enter your params in line separated by space, like this: key1=val1 key2=val2")
        if ( line == '' ):
            return
        #splitedLine = line.Split( ' ' ).Select(n=> {             CHANGE THIS!!!
        #    if ( !n.Contains( "=" ) )
        #        return new KeyValuePair<PaytureParams, dynamic>(PaytureParams.Unknown, null);
        #    var temp = n.Split( '=' );
        #    PaytureParams paytureParam = PaytureParams.Unknown;
        #    if ( !Enum.TryParse( temp[ 0 ], true, out paytureParam ) )
        #        return new KeyValuePair<PaytureParams, dynamic>(PaytureParams.Unknown, null);
        #    return new KeyValuePair<PaytureParams, dynamic>( paytureParam, temp[ 1 ] );
        #} );
        #
        #foreach(var keyVal in splitedLine)
        #    if(allFields.ContainsKey(keyVal.Key))
        #        allFields[ keyVal.Key ] = keyVal.Value;


    def listCommands(self):
        print("Commands for help:\n\n" + 
                            "* fields - list current key-value pairs that used in request to Payture server.\n\n" +
                            "* changefields - command for changing current values of  key-value pairs that used in request to Payture server.\n\n" + 
                            "* commands - list avaliable commands for this console program.\n\n" + 
                            "* changemerchant - commands for changing current merchant account settings.\n\n" +
                            "* help - commands that types this text (description of commands that you can use in this console program.).\n\n\n" )
        print("Commands for invoke PaytureAPI functions.\n" +
                "* pay - use for one-stage payment. In EWALLET an INPAY api this command can be use for block funds - if you specify SessionType=Block.\n\n" +
                "* block - use for block funds on Customer card. After that command the funds can be charged by Charge command or unblocked by Unblock command. This command use only for API.\n\n" + 
                "* charge - write-off of funds from customer card.\n\n" + 
                "* unblock - unlocking of funds on customer card.\n\n" +
                "* refund - operation for refunds.\n\n" + 
                "* getsstate - use for getting the actual state of payments in Payture processing system. This command use only for API.\n\n" +
                "* paystatus - use for getting the actual state of payments in Payture processing system. This command use for EWALLET and INPAY.\n\n" + 
                "* init - use for payment initialization, customer will be redirected on Payture payment gateway page for enter card's information.\n\n" + 
                "* register - register new customer. This command use only for EWALLET.\n\n" +
                "* check - check for existing customer account in Payture system. This command use only for EWALLET.\n\n" + 
                "* update - This command use only for EWALLET.\n\n" + 
                "* delete - delete customer account from Payture system. This command use only for EWALLET.\n\n" +
                "* add - register new card in Payture system. This command use only for EWALLET.\n\n" +
                "* activate - activate registered card in Payture system. This command use only for EWALLET.\n\n" +   
                "* sendcode - provide additional authentication for customer payment. This command use only for EWALLET.\n\n" +
                "* remove - delete card from Payture system. This command use only for EWALLET.\n\n" )
        return

    def changeMerchant(self):
        _merchantKey = input('Type Merchant account name: ')
        _merchantPassword = input('Type Merchant account password: ')
        _host = input('Type host name: ')
        print( "Merchant account settings: \n\tMerchantName=%s\n\tMerchantPassword=%s\n\tHOST=%s\n" % (_merchantKey, _merchantPassword, _host) )
        self.Merchant = Merchant( _merchantKey, _merchantPassword, _host )
        return

    def help(self):
        print("\n\nThen console promt you 'Type command' - you can type commands for invoke PaytureAPI functions and you can types commands for help.")
        print("After you type the command an appropriate method will be execute. If the data is not enough for execute the program promt for additional input.")
        

    def writeResult(self):
        if(self.response != None):
            print (self.response)


    def generateOrderId(self):
        self.allFields[ PaytureParams.OrderId ] = "ORD_%s_TEST" % (self.rand.randint( 0, 1000000000 ))

    def generateAmount(self):
        self.allFields[ PaytureParams.Amount ] = '%s' % ( self.rand.randint( 50, 100000 ))
