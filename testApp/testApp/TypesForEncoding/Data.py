from EncodeString import *

class Data(EncodeString):
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


