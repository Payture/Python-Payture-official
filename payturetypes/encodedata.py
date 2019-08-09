import string

class EncodeString(object):
    def __init__(self, **kwargs):
        super(EncodeString, self).__init__()

    def _getPropertiesString(self):
        listattrs = dir(self)
        result = ""
        for elem in listattrs:
            if(elem.startswith('_') or elem.endswith('_')):
                continue
            result += elem + '=' + str(getattr(self, elem)) + ';'
        return result


class PayInfo(EncodeString):

    def __init__(self, pan, emonth, eyear, cardHolder, secureCode, orderId, amount):
        self.PAN = pan
        self.EMonth = emonth
        self.EYear = eyear
        self.CardHolder = cardHolder
        self.SecureCode = secureCode
        self.OrderId = orderId
        self.Amount = amount
        super(PayInfo, self).__init__()


class Card(EncodeString):
    def __init__(self, cardNum, eMonth, eYear, cardHolder, secureCode, cardId = None ):
        self.CardNumber = cardNum
        self.EMonth = eMonth
        self.EYear = eYear
        self.CardHolder = cardHolder
        self.SecureCode = secureCode
        self.CardId = cardId
        super(Card, self).__init__()


class Customer(EncodeString):
    def __init__(self, login, password, phone=None, email=None):
        self.VWUserLgn = login
        self.VWUserPsw = password
        self.PhoneNumber = phone
        self.Email = email
        super(Customer, self).__init__()

class Data(EncodeString):
    def __init__(self, sessionType, ip, **kwargs):
        self.SessionType = sessionType
        self.IP = ip
        for key, value in kwargs.items():
            if(key == 'OrderId'):
                self.OrderId = value
            elif(key == 'Amount'):
                self.Amount = value
            elif(key == 'Language'):
                self.Language = value
            elif(key == 'TemplateTag'):
                self.TemplateTag = value
            elif(key == 'Url'):
                self.Url = value
            elif(key == 'Product'):
                self.Product = value
            elif(key == 'Total'):
                self.Total = value
            elif(key == 'ConfirmCode'):
                self.ConfirmCode = value
            elif(key == 'CustomFields'):
                self.CustomFields = value
        super(Data, self).__init__()


