from EncodeString import *


class PayInfo(EncodeString):

    def __init__(self, pan, emonth, eyear, cardHolder, secureCode, orderId, amount):
        self.PAN = pan
        self.EMonth = emonth
        self.EYear = eyear
        self.CardHolder = cardHolder
        self.SecureCode = secureCode
        self.OrderId = orderId
        self.Amount = amount

