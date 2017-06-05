from EncodeString import *

class Data(EncodeString):

    def __init__(self, sessionType, orderId, amount, ip,  product,  total, url, template, lang, confirmCode,  customFields ):
        self.SessionType = sessionType
        self.IP = ip
        self.OrderId = orderId
        self.Amount = amount
        self.Language = lang
        self.TemplateTag = template
        self.Url = url
        self.Product = product
        self.Total = total
        self.ConfirmCode = confirmCode
        self.customFields = customFields


    def __init__(self, sessionType, ip,  **kwargs):
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


