# Python-Payture-official

This is Offical Payture API for Python. To get started you will need a Merchant account, please contact our support to get one. Here you can explore how to use our API functions! Let's go!

## Install
Simple to install (please note, this is test module now - we're working to improve this :) ):  
```pip
pip install payture
```
And include to your project:
```python
import payture
```

## Payture API tutorial
Before fall into the deep, we're need to provide you general conception of working with our API function. See picture: 
![](generalCSharp.jpg) 

## [Steps](#newMerchant)

 * [Creating merchant account](#newMerchant)
 * [Get access to required API](#accessToAPI)
 * [Expand transaction](#expandTransaction)
 * [Send request](#sendRequest)

## [Base Types](#baseTypes)
* [PayInfo](#PayInfo)
* [Card](#Card)
* [Data](#Data)
* [PaytureCommands](#PaytureCommands)
* [Customer](#Customer)
* [PaytureResponse](#PaytureResponse)
* [CardInfo](#CardInfo)
* [Transaction](#Transaction)

## [Test App](#testApp)

Now, let's walk through the steps from the picture above



## First Step - Creating Merchant Account <a id="newMerchant" ></a>
To get access for API usage just create the instance of Merchant object, pass in the constructor the name of the host, name of your account and your account password.  Suppose that you have Merchant account with  name: Key = "MyMerchantAccount" and password Password = "MyPassword".

Pass the 'https:#sandbox.payture.com' for test as the name of Host (first parameter).
```python
merchant = Merchant("https://sandbox.payture.com", "MyMerchantAccount", "MyPassword")
```
We're completed the first step! Go next!
***
Please note, that  Key = "'MyMerchantAccount" and Password = "MyMerchantAccount"  - fake, [our support](http://payture.com/kontakty/) help you to get one!
***

## Second Step - Get access to required API <a id="accessToAPI" ></a>
At this step you just call one of following methods on Merchant object (which provide proper API type for you) and pass in the PaytureCommands [see description here](#PaytureCommands): 
* Api (this is PaytureAPI)
```python
transaction = merchant.api( PaytureCommands.Pay )
```
* InPay (this is PaytureInPay)
```python
transaction = merchant.inpay( PaytureCommands.Pay )
```
* EWallet (this is PaytureEWallet)
```python
transaction = merchant.ewallet( PaytureCommands.Init )
```
* Apple (this is PaytureApplePay)
And pass in the [PaytureCommands](#PaytureCommands).
```python
transaction = merchant.apple( PaytureCommands.Pay )
```
* Android (this is PaytureAndroidPay)
And pass in the [PaytureCommands](#PaytureCommands).
```python
transaction = merchant.android( PaytureCommands.Pay )
```
Result of this methods is the instanse of Transaction object (with emty data set) which you expand in the next step. 

 [See this table](#PaytureCommandsTable) for explore what PaytureCommands received  theese methods.

## Third Step - Expand transaction <a id="extpandTransaction" ></a>
At this step you needed to chose an appopriate method for set data and futher sending to Payture server.
In the previous step we get the special for api Transaction object [see here that is it](#Transaction). You need expand it, below you find detailed description how do this for every type of api.


###  expand(orderId, amount)
This overload available in any of the API type

Call this for following PaytureCommands:
* Unblock
* Refund
* Charge
* GetState (PaytureAPI)
* PayStatus (PaytureEWallet, PaytureInPay)

| Parameter's name | Definition                                                        |
| ---------------- | ----------------------------------------------------------------- |
| orderId          | Payment identifier in your service system.                        |
| amount           | Amount of payment kopec. (in case of GetState or PayStatus pass null)                                          |


Example for Charge:

> Note Charge operation we're can make after the funds on Customer's card was blocked.
```python
orderId = "TESTORD000000000000000000" # pass in the transaction's OrderId used in PaytureCommands.Block operation.
amount = 7444444                      # transaction's Amount used in PaytureCommands.Block

# Create and expand transaction for Api:
payTransactionApi = merchant.api( PaytureCommands.Charge ).expand( orderId, amount )

# Create and expand transaction for InPay:
payTransactionInPay = merchant.inpay( PaytureCommands.Charge ).expand( orderId, amount )

# Create and expand transaction for EWallet:
payTransactionEWallet = merchant.ewallet( PaytureCommands.Charge ).expand( orderId, amount )
```

### Expand Transaction Methods for PaytureAPI
#### expandPayBlock(info, customFields, customerKey, paytureId)
This overload you call for api methods:
* **Pay** (PaytureCommands.Pay).
* **Block**  (PaytureCommands.Block).

Description of provided params.

| Parameter's name | Definition                                                                             |
| ---------------- | -------------------------------------------------------------------------------------- |
| info             | Params for transaction processings [see here for explore PayInfo object](#PayInfo)     |
| customerKey      | Customer identifier in Payture AntiFraud system.                                       |
| customFields     | Additional fields for processing (especially for AntiFraud system).                    |
| paytureId        | Payments identifier in Payture AntiFraud system.                                       |


Example for Pay:
```python
payinfo = PayInfo(
    "4111111111111112",             # card number, required
    "10",                           # expiration month, required
    "20",                           # expiration year, required
    "Test Test",                    # cardholder name, required
    "123",                          # secure code, required
    "TestOrder0000000000512154545", # payment's identifier in Merchant system
    41000                           # amount, required
)
customFields = {
    'IP' : '93.120.05.36' ,
    'Description' : 'SomeUsefullHere' 
} # optional, can be None 

customerKey = "testKey"     # needed for AntiFraud check 
paytureId = ""              # optional 

# Create and expand transaction 
payTransaction = merchant.api( PaytureCommands.Pay ).expandPayBlock( payInfo, customFields, customerKey, paytureId )
```

### ExpandTransaction Methods for PaytureInPay
#### expandInit(data)
This overload you call for api **Init** method ( PaytureCommands.Init )
Full description of recieved [data see here](#Data).
You must specify following fields of Data object then call Init api method of PaytureInPay:
* SessionType (maybe Pay or Block)
* OrderId
* Amount
* IP

Other fields is optional. Example:
```python
orderId = "TESTORD000000000000000000"
amount = 102000  # in kopecs
ip = "93.45.120.14"
data = Data( SessionType.Pay, ip { 'OrderId' : orderId, 'Amount' : amount } )

# Create and expand transaction 
initTransaction = merchant.inpay( PaytureCommands.Init ).expandInit( data )
```
> Please note that the response from Init method will be contain SessionId - the unique payment's identifier - further you need to use it in PaytureCommands.Pay  api method for proseccing transaction on Payture side: call manually (suppose, we're have sessionId value from Init):
*  merchant.inpay( PaytureCommands.Pay ).expandSessionId( sessionId ) - use for SessionType=Pay or SessionType=Block

> To do the same thing you can take value from response's RedirectURL property - which is string representation of Url constracted for you (a value in RedirectURL will be set only in PaytureCommands.Init response, in over cases it has null value)  - and just redirect customer to this address.


### ExpandTransaction Methods for PaytureEWallet
#### expandInit(customer, cardId, data ) 
This overload you call for api 
* **Init** (PaytureCommands.Init). 

Example for SessionType=Pay and SessionType=Block:
```python
cardId = "40252318-de07-4853-b43d-4b67f2cd2077"
customer = Customer( "testCustomerEW", "testPass" )
sessionType = SessionType.Pay                       # = SessionType.Block,  required
orderId = "TESTORD000000000000000000"               # required
amount = 102000                                     # in kopec, required
ip = "93.45.120.14"                                 # required
product = "SomeCoolProduct"                         # optional, maybe  None 
total = amount                                      # optional, maybe  None
template = "tempTag"                                # optional, maybe  None
lang = "RU"                                         # optional, maybe  None
data = Data ( sessionType, ip, { 'OrderId' : orderId, 'Amount' : amount,  'Product' : product, 'Total' : total, 'Tamplate' : template, 'Language' : lang } ) # required

# Create and expand transaction 
initPayTransaction = merchant.ewallet( PaytureCommands.Init ).expandInit( customer, cardId, data ) # SessionType=Pay or SessionType=Block
```


Example for SessionType=Add:
```python
cardId = None  # we're pass None for Add SessionType
customer =  Customer( "testCustomerEW", "testPass" )
sessionType = SessionType.Add # required
ip = "93.45.120.14"           # required
template = "tempTag"          # optional, maybe None
lang = "RU"                   # optional, maybe None
data =  Data( sessionType, ip, { 'TemplateTag' : template, 'Language' : lang } ) # required

# Create and expand transaction 
initAddTransaction = merchant.ewallet( PaytureCommands.Init ).expandInit( customer, None, data ); # SessionType=Add
```

> Please note that the response from Init method will be contain SessionId - the unique payment's identifier - further you need to use it in PaytureCommands.Pay or PaytureCommands.Add api methods for proseccing transaction on Payture side: call manually (suppose, we're have sessionId value from Init):
*  merchant.ewallet( PaytureCommands.Pay ).expandSessionId( sessionId ) - use for SessionType=Pay or SessionType=Block
*  merchant.ewallet( PaytureCommands.Add ).expandSessionId( sessionId ) - use for SessionType=Add 

> To do the same thing you can take value from response's RedirectURL property - which is string representation of Url constracted for you (a value in RedirectURL will be set only in PaytureCommands.Init response, in over cases it has null value)  - and just redirect customer to this address.

#### expandForMerchantPayReg(customer, cardId, secureCode, data) 
This overload you call for api 
* **Pay** (PaytureCommands.Pay) - on Merchant side for REGISTERED card

Example for SessionType=Pay and SessionType=Block:
```python
sessionType = SessionType.Pay                       # = SessionType.Block,  required
orderId = "TESTORD000000000000000000"               # required
cardId = "40252318-de07-4853-b43d-4b67f2cd2077"     # required
secureCode = 123                                    # required
amount = 102000                                     # in kopec, required
ip = "93.45.120.14"                                 # required
confirmCode = "SomeCoolProduct"                     # optional, maybe None
customFields = ""                                   # optional maybe None
customer = Customer( "testCustomerEW", "testPass" ) # required
data = Data ( sessionType, ip, { 'OrderId': orderId, 'Amount' : amount, 'ConfirmCode' : confirmCode, 'CustomFields' : customFields } )    # required

# Create and expand transaction 
payTransaction = merchant.ewallet( PaytureCommands.Pay ).expandForMerchantPayReg( customer, cardId, secureCode, data )

```
#### expandForMerchantPayNoReg(customer, card, data) 
This overload you call for api 
* **Pay** (PaytureCommands.Pay) - on Merchant side for NOT REGISTERED card

Example for SessionType=Pay and SessionType=Block:
```python
sessionType = SessionType.Pay           # = SessionType.Block,  required
orderId = "TESTORD000000000000000000"   # required
amount = 102000                         # in kopec, required
ip = "93.45.120.14"                     # required
confirmCode = "SomeCoolProduct"         # optional, maybe None
customFields = ""                       # optional maybe None
data = Data ( sessionType, ip, { 'OrderId': orderId, 'Amount' : amount, 'ConfirmCode' : confirmCode, 'CustomFields' : customFields } )    # required

customer = Customer( "testCustomerEW", "testPass" ) #required

card =  Card( 
    "4111111111111112", # card number
    10,                 # expiration month
    20,                 # expiration year
    "Card Holder",      # CardHolder Name
    111,                # secure code
)                       # required

# Create and expand transaction 
payTransaction = merchant.ewallet( PaytureCommands.Pay ).expandForMerchantPayNoReg( customer, card, data )

```

#### expandForMerchantAdd(customer, card)
This overload you call for api
* **Add** method ( PaytureCommand.Add ) on Merchant side.

Example:
```python
customer = Customer( "testCustomerEW", "testPass" ) #required
card = Card( 
    "4111111111111112", # card number
    10,                 # expiration month
    20,                 # expiration year
    "Card Holder",      # CardHolder Name
    111,                # secure code
)                       # required

# Create and expand transaction 
addTransaction = merchant.ewallet( PaytureCommands.Add ).expandForMerchantAdd( customer, card )
```

Please note, that you can add card *only for registered customer*.


#### expandCustomer(customer)
This overload is called for following api methods:

* **Register** (PaytureCommands.Register),
* **Update** (PaytureCommands.Update), 
* **Delete** (PaytureCommands.Delete), 
* **Check** (PaytureCommands.Check), 
* **GetList** (PaytureCommands.GetList)
Description of recieved [Customer data see here](#Customer).

Example for PaytureCommands.Register:
```python
customer = Customer( 
    "testCustomerEW", # login, required
    "testPass",       # password, required
    "78456865353",    # phone, optional
    "newCustTest@gmailTest@.ru" # email, optional
     )

# Create and expand transaction      
registerTransaction = merchant.ewallet( PaytureCommands.Reqister ).expandCustomer( customer )
```



#### expandForCardOperation(customer, cardId, amount, orderId = None)
This overload is called for api methods: 
* **SendCode** (PaytureCommands.SendCode). You need to specify all parameters include orderId.
Example:
```python
customer = Customer( "testCustomerEW", "testPass" )
cardId = "40252318-de07-4853-b43d-4b67f2cd2077"
amount = 50000
orderId = "TESTORD000000000000000000"

# Create and expand transaction 
sendCodeTransaction = merchant.ewallet( PaytureCommands.SendCode ).expandForCardOperation( customer, cardId, amount, orderId )
```
* **Activate** (PaytureCommands.Activate). Specify customer, cardId and amount for this operation.
Example:
```python
customer = Customer( "testCustomerEW", "testPass" )
cardId = "40252318-de07-4853-b43d-4b67f2cd2077"
amount = 100 # pass small amount for activate

# Create and expand transaction 
activateTransaction = merchant.ewallet( PaytureCommands.Activate ).expandForCardOperation( customer, cardId, amount )
```
* **Remove** (PaytureCommands.Remove). You need to specify customer and cardId only for this operation. For amount pass None.
Example:
```python
customer = new Customer( "testCustomerEW", "testPass" )
cardId = "40252318-de07-4853-b43d-4b67f2cd2077"

# Create and expand transaction 
removeTransaction = merchant.ewallet( PaytureCommands.Remove ).expandForCardOperation( customer, cardId, None )
```


#### expandSessionId(sessionId)
This overload is called for api methods: 
* **Pay** (PaytureCommands.Pay). On Payture side
* **Add** (PaytureCommands.Add). On Payture side

Example for PaytureCommands.Pay:
```python
sessionId = "e5c43d9f-2646-42bc-aeec-0b9005ceb972"; # received from PaytureCommands.Init 

# Create and expand transaction 
payTransaction = merchant.ewallet( PaytureCommands.Pay ).expandSessionId( sessionId )
```

#### expandPaySubmit3DS(MD, paRes)
This overload is called for api methods: 
* **PaySubmut3DS** (PaytureCommands.PaySubmit3DS).
Example for:
```python
md = "20150624160356619170 " # received from ACS 
pares = "ODJhYTk0NGUtMDk0ZlKJjjhbjlsrglJKJHNFKSRFLLkjnksdfjgdlgkd.... " # received from ACS 

# Create and expand transaction 
paySubmitTransaction = merchant.ewallet( PaytureCommands.PaySubmit3DS ).expandPaySubmit3DS( md, pares )
```

### ExpandTransaction Methods for PaytureApplePay and PaytureAndroidPay
#### expandPayBlock(payToken, orderId, amount)
This overload you call for:
* **Pay** (PaytureCommands.Pay) 
* **Block** (PaytureCommands.Block) 
Description of provided params.

| Parameter's name | Definition                                                                             |
| ---------------- | -------------------------------------------------------------------------------------- |
| payToken         | PayToken for current transaction.   |
| orderId          | Current transaction OrderId, if you miss this value (if pass null) - it will be generate on Payture side.    |
| amount           | Current transaction amount in kopec (pass null for ApplePay).                      |



## Last Step - Send request <a id="sendRequest" ></a>
After transaction is expanded you can send request to the Payture server via one of two methods:
* processSync() - this is sync method. The executed thread will be block while waiting response from the server - return the PaytureResponse object.


## Base Types <a id="baseTypes"></a>:

### PayInfo <a id="PayInfo"></a>
This object used for PaytureAPI and consist of following fields:

| Fields's name    | Definition                                      |
| ---------------- | ----------------------------------------------- |
| OrderId          | Payment identifier in your service system.      |
| Amount           | Amount of payment kopec.                        |
| PAN              | Card's number.                                  |
| EMonth           | The expiry month of card.                       |
| EYear            | The expiry year of card.                        |
| CardHolder       | Card's holder name.                             |
| SecureCode       | CVC2/CVV2.                                      |

You can use following constructor for creation PayInfo object:
```python
info = PayInfo( 
    "4111111111111112", # PAN
    10,                 # EMonth
    20,                 # EYear
    "Test Test",        # CardHolder
    123,                # SecureCode
    "TestOrder0000000000512154545", # OrderId
    580000              # Amount 
    )
```

### Card <a id="Card"></a>
This object used for PaytureEWallet and consist of following fields:

| Fields's name    | Definition                                      |
| ---------------- | ----------------------------------------------- |
| CardId           | Card identifier in Payture system.              |
| CardNumber       | Card's number.                                  |
| EMonth           | The expiry month of card.                       |
| EYear            | The expiry year of card.                        |
| CardHolder       | Card's holder name.                             |
| SecureCode       | CVC2/CVV2.                                      |

Examples of creation instance of Card:
```python
card = Card( "4111111111111112", 10, 20, "Test Test", 123 )  #create card with CardId = None
cardWithId = Card( "4111111111111112", 10, 20, "Test Test", 123, "40252318-de07-4853-b43d-4b67f2cd2077" ) # create card with CardId = "40252318-de07-4853-b43d-4b67f2cd2077"
```
### Data <a id="Data"></a>
This is object used for PaytureEWallet and PaytureInPay, consist of following fields 

| Fields's name    | Definition                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| SessionType      | Session Type - determines the type of operation. In this object - it's string representation of SessionType enum.   |
| IP               | Customer's IP adress.                                                                                               |
| TemplateTag      | Tamplate which used for payment page.                                                                               | 
| Language         | Addition parameter for determining language of template.                                                            |
| OrderId          | Payment identifier in your service system.                                                                          |
| Amount           | Amount of payment kopec.                                                                                            |
| Url              | The address to which Customer will be return after completion of payment.                                           |
| Product          | Name of product.                                                                                                    | 
| Total            | Total Amount of purchase.                                                                                           |
| ConfirmCode      | Confirmation code from SMS. Required in case of confirm request for current transaction.                            |
| CustomFields     | Addition transaction's fields.                                                                                      |

Examples of creation instance of Data:
```python
# Data(sessionType, ip, **kwargs) 
# in **kwargs pass only fields in which you intresting in
data = Data( 
    SessionType.Pay, # SessionType.Pay - for one-stage operation; SessionType.Block - for two-stage operation; SessionType.Add - for adding card (PaytureEWallet)
    "127.0.0.1",     # IP
    {
        'OrderId' : 'TestOrder0000000000512154545',
        'Amount' : 20000, 
        'Total' : 20000,
        'Product' : 'ProductName',
        'TemplateTag' : 'Tag',
        'Language' : 'RU'
        'Url' : 'http://returncustomer.ru',
        'CustomFields' : 'SomeField=FieldValue;AnotherField=AnotherValue;AndLastAddition=LastValue;'
        'ConfirmCode' : 1244555
    }
)
```

### PaytureCommands <a id="PaytureCommands"></a>
This is enum of **all** available commands for Payture API.

PaytureCommands list and availability in every api type

| Command      | Api | InPay | EWallet | Apple | Android | Description                                                                                                            |
| ------------ | --- | ----- | ------- | ----- | ------- | ---------------------------------------------------------------------------------------------------------------------- |
| Pay          |  +  |   +   |    +    |   +   |    +    | Command for pay transaction. In InPay and EWallet can be used for Block operation                                      |
| Block        |  +  |       |         |   +   |    +    | Block of funds on customer card. You can write-off of funds by Charge command or unlocking of funds by Unblock command |
| Charge       |  +  |   +   |    +    |       |         | Write-off of funds from customer card                                                                                  |
| Refund       |  +  |   +   |    +    |       |         | Operation for refunds                                                                                                  |
| Unblock      |  +  |   +   |    +    |       |         | Unlocking of funds  on customer card                                                                                   |
| GetState     |  +  |       |         |       |         | Get the actual state of payments in Payture processing system                                                          |
| Init         |     |   +   |    +    |       |         | Payment initialization, customer will be redirected on Payture payment gateway page for enter card's information       |
| PayStatus    |     |   +   |    +    |       |         | Get the actual state of payments in Payture processing system                                                          |
| Add          |     |       |    +    |       |         | Register new card in Payture system                                                                                    |
| Register     |     |       |    +    |       |         | Register new customer account                                                                                          |
| Update       |     |       |    +    |       |         | Update customer account                                                                                                |
| Check        |     |       |    +    |       |         | Check for existing customer account in Payture system                                                                  |
| Delete       |     |       |    +    |       |         | Delete customer account from Payture system                                                                            |
| Activate     |     |       |    +    |       |         | Activate registered card in Payture system                                                                             |
| Remove       |     |       |    +    |       |         | Delete card from Payture system                                                                                        |
| GetList      |     |       |    +    |       |         | Return list of registered cards for the customer existed in Payture system                                             |
| SendCode     |     |       |    +    |       |         | Additional authentication for customer payment                                                                         |
| Pay3DS       |  +  |       |         |       |         | Command for one-stage charge from card with 3-D Secure                                                                 |
| Block3DS     |  +  |       |         |       |         | Block of funds on customer card with 3-D Secure                                                                        |
| PaySubmit3DS |     |       |    +    |       |         | Commands for completed charging funds from card with 3-D Secure                                                        |


### Customer <a id="Customer"></a>
This object used for PaytureEWallet and consist of following fields:

| Fields's name    | Definition                                                       |
| ---------------- | ---------------------------------------------------------------- |
| VWUserLgn        | Customer's identifier in Payture system. (Email is recommended). |
| VWUserPsw        | Customer's password in Payture system.                           |
| PhoneNumber      | Customer's phone number.                                         |
| Email            | Customer's email.                                                |

```python
customer = Customer( "testLogin@mail.com", "customerPassword") #create customer without phone and email
customer2 = Customer( "testLogin@mail.com", "customerPassword", "77125141212", "testLogin@mail.com" ) #customer with all fields
```


### PaytureResponse <a id="PaytureResponse"></a>
This object is response from the Payture server and consist of following fields:

| Fields's name    | Definition                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| APIName          | Name of commands that was called.                                                                |
| Success          | Determines the success of processing request.                                                    |
| ErrCode          | Will be contain code of error if one occur during process the transaction on the Payture server. | 
| RedirectURL      | Will be contain the new location for redirect. (for PaytureCommands.Init).                       |
| Attributes       | Addition attributes from the response.                                                           |
| InternalElements | Additional information from the response.                                                        |
| ListCards        | List of cards, theese registered for current Customer (this field filled for PaytureCommands.GetList)  |
| ResponseBodyXML  | String representation received from Payture server in XML format                                 |


### CardInfo <a id="CardInfo"></a>
Special object for containing Customer card's information, that we're received from PaytureCommands.GetList command

| Fields's name    | Definition                                                             |
| ---------------- | ---------------------------------------------------------------------- |
| CardNumber       | The masked card's number.                                              |
| CardId           | Card identifier in Payture system.                                     |
| CardHolder       | Name of card's holder                                                  | 
| ActiveStatus     | Indicate of card's active status in Payture system                     |
| Expired          | Indicate whether the card expired on the current date                  |
| NoCVV            | Indicate whether or not payment without CVV/CVC2                       |

### Transaction <a id="Transaction"></a>
You don't needed to create object of this type by yoursef - it will be created for you then you access to appopriate API via Merchant object. 
This object contans the necessary fields which used in request construction process. And this is abstract type.



## Test application <a id="testApp"></a>
You can download simple test application - realized as console app - and test work of our API just type the command in command line. Full description of command for app available into app by the command help. And then the app starts - it ask you for necessity of assistance.


Visit our [site](http://payture.com/) for more information.
You can find our contact [here](http://payture.com/kontakty/).