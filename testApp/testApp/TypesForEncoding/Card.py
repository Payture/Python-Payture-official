from EncodeString import *

class Card(EncodeString):
    def __init__(self, cardNum, eMonth, eYear, cardHolder, secureCode, cardId = None ):
        self.CardNumber = cardNum
        self.EMonth = eMonth
        self.EYear = eYear
        self.CardHolder = cardHolder
        self.SecureCode = secureCode
        self.CardId = cardId
        return super().__init__(self)