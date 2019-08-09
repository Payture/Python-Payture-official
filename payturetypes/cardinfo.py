class CardInfo(object):

    def __init__(self, cardNumber, cardId, cardHolder, activeStatus, expired, nocvv):
        self.CardNumber = cardNumber
        self.CardId = cardId
        self.CardHolder = cardHolder
        self.ActiveStatus = activeStatus
        self.Expired = expired
        self.NoCVV = nocvv
        super(CardInfo, self).__init__()
