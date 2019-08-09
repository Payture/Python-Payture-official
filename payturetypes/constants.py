
class PaytureCommands(object):
    Unknown = 'Unknown'
    Pay = 'Pay'
    Block = 'Block'
    Unblock = 'Unblock'
    Charge = 'Charge'
    Refund = 'Refund'
    GetState = 'GetState'
    PayStatus = 'PayStatus'
    Init = 'Init'
    Add = 'Add'
    Pay3DS = 'Pay3DS'
    Block3DS = 'Block3DS'
    Register = 'Register'
    Delete = 'Delete'
    Check = 'Check'
    Activate = 'Activate'
    Remove = 'Remove'
    SendCode = 'SendCode'
    GetList = 'GetList'
    ApplePay = 'ApplePay'
    AndroidPay = 'AndroidPay'
    Update = 'Update'
    PaySubmit3DS = 'PaySubmit3DS'

    def __setattr__(self, *_):
        pass





class PaytureParams(object):
	VWUserLgn = 'VWUserLgn'
	VWUserPsw = 'VWUserPsw'
	CardId = 'CardId'
	IP = 'IP'
	DATA = 'DATA'
	Key = 'Key'
	PayInfo = 'PayInfo'
	VWID = 'VWID'
	Amount = 'Amount'
	SessionId = 'SessionId'
	CardNumber = 'CardNumber'
	EMonth = 'EMonth'
	EYear = 'EYear'
	CardHolder = 'CardHolder'
	SecureCode = 'SecureCode'
	PhoneNumber = 'PhoneNumber'
	Password = 'Password'
	Email = 'Email'
	OrderId = 'OrderId'
	SessionType = 'SessionType'
	Data = 'Data'
	PAN = 'PAN'
	CustomerKey = 'CustomerKey'
	PaytureId = 'PaytureId'
	CustomFields = 'CustomFields'
	Description = 'Description'
	PaRes = 'PaRes'
	MD = 'MD'
	PayToken = 'PayToken'
	Method = 'Method'
	TemplateTag = 'TemplateTag'
	Language = 'Language'
	Product = 'Product'
	Total = 'Total'
	Url = 'Url'
	Unknown = 'Unknown'

	def __setattr__(self, *_):
		pass


class PaytureAPIType(object):
	api = 'api'
	apim = 'apim'
	vwapi = 'vwapi'

	def __setattr__(self, *_):
		pass




class DigitalPayMethods(object):
	PAY = 'PAY'
	BLOCK = 'BLOCK'

	def __setattr__(self, *_):
		pass

class SessionType(object):
	Add = 'Add'
	Pay = 'Pay'
	Block = 'Block'
	Unknown = 'Unknown'

	def __setattr__(self, *_):
		pass

