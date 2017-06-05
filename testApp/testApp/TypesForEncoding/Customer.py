from EncodeString import *

class Customer(EncodeString):
	
    def __init__(self, login, password, phone=None, email=None):
        self.VWUserLgn = login
        self.VWUserPsw = password
        self.PhoneNumber = phone
        self.Email = email


