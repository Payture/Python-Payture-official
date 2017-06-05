from RequestClient import *
from Constants import *
import string
from PaytureResponse import *
import urllib.parse

class Transaction(RequestClient):

	def __init__(self, api, command, merchant):
		self._apiType = api
		self._sessionType = SessionType.Unknown;
		self._merchant = merchant
		self._expanded = False
		self.Command = command
		self._requestKeyValuePair = {}

    # <summary>
    # Expand transaction for API Methods: Charge/UnBlock/Refund/GetState  
    # for Ewallet and InPay Methods: Charge/UnBlock/Refund/PayStatus  
    # </summary>
    # <param name="orderId">Payment's identifier in Merchant system</param>
    # <param name="amount">Payment's amount in kopec. Pass null for PayStatus and GetState commands</param>
    # <returns></returns>
	def expand(self, orderId, amount):
		if(self._expanded):
			return self
		if(orderId == ''):
			return self

		if(self._apiType == PaytureAPIType.vwapi):
			if(self.Command == PaytureCommands.PayStatus):
				self._requestKeyValuePair[PaytureParams.DATA] = '%s=%s;'%(PaytureParams.OrderId, orderId)
			elif(self.Command == PaytureCommands.Refund and amount != None):
				self._requestKeyValuePair[PaytureParams.DATA] = '%s=%s;%s=%s;%s=%s;'%(PaytureParams.OrderId, orderId, PaytureParams.Amount, amount, PaytureParams.Password, self._merchant.Password)
			elif(amount != None):
				self._requestKeyValuePair[PaytureParams.Amount] = amount
			else:
				self._requestKeyValuePair[PaytureParams.OrderId] = orderId
		else:
			self._requestKeyValuePair[PaytureParams.OrderId] = orderId
			if(amount != None):
				self._requestKeyValuePair[PaytureParams.Amount] = amount

		if(self.Command == PaytureCommands.Refund or (self._apiType != PaytureAPIType.api and (self.Command == PaytureCommands.Charge or self.Command == PaytureCommands.Unblock))):
			expandMerchant(true, true)
		else:
			expandMerchant()

		self._expanded = True
		return self;



	# <summary>
    # Expand transaction with Merchant key and password
    # </summary>
    # <param name="addKey">Pass False if Merchant key IS NOT NEEDED.</param>
    # <param name="addPass">Pass true if Merchant password IS NEEDED.</param>
    # <returns>return current expanded transaction</returns>
	
	def expandMerchant(self, addKey = True, addPass = False ):
		if(addKey):
			self._requestKeyValuePair[(PaytureParams.VWID if self._apiType == PaytureAPIType.vwapi else  PaytureParams.Key)] = self._merchant.MerchantName
		if(addPass):
			self._requestKeyValuePair[PaytureParams.Password] = self._merchant.Password
		return self



	# <summary>
    # Form content for request
    # </summary>
    # <returns></returns>
	def formContent(self):
		return self._requestKeyValuePair
        # return new FormUrlEncodedContent( _requestKeyValuePair.Where( n=>n.Value != null ).Select( n => new KeyValuePair<string, string>( n.Key.ToString(), $"{n.Value}" ) ) );

	def processAsync(self):
		if(self._expanded == False):
			return PaytureResponse.PaytureResponse.errorResponse(self.Command, 'Params are not set')
		#if ( Command == PaytureCommands.Init )
        #return await PostAsync( GetPath(), FormContent() ).ContinueWith( r => ParseResponseInternal( r, Command, SessionType ) ).ContinueWith( r => FormRedirectURL( r ) );
		#return await PostAsync( GetPath(), FormContent() ).ContinueWith( r => ParseResponseInternal( r, Command, SessionType ) );
		return self.post(self.getPath(),self.formContent()) #??????????????????????????

	# <summary>
	# Process request to Payture server synchronously
	# </summary>
	# <returns>PaytureResponse - response from the Payture server. In case of exeption will be return PaytureResponse with exeption mesage in ErrCode field.</returns>
	def processSync(self):
		if(self._expanded == False):
			return PaytureResponse.PaytureResponse.errorResponse(self.Command, 'Params are not set')
		#if ( Command == PaytureCommands.Init )
        #{
        #    try {
        #        var operationResult = PostAsync( GetPath(), FormContent() ).ContinueWith( r => ParseResponseInternal( r, Command, SessionType ) ).ContinueWith( r => FormRedirectURL( r ) );
        #       operationResult.Wait();
        #        return operationResult.Result;
        #    }
        #    catch(Exception ex )
        #    {
        #        return PaytureResponse.ErrorResponse( this, $"Error occurs{Environment.NewLine}Message: [{ex.Message}]{Environment.NewLine}StackTrace: {ex.StackTrace}");
        #    }
        #}
        #else
        #{
        #    try
        #    {
        #        var operationResult = PostAsync( GetPath(), FormContent() ).ContinueWith( r => ParseResponseInternal( r, Command, SessionType ) );
        #        operationResult.Wait();
        #        return operationResult.Result;
        #    }
        #    catch(Exception ex)
        #    {
        #        return PaytureResponse.ErrorResponse( this, $"Error occurs{Environment.NewLine}Message: [{ex.Message}]{Environment.NewLine}StackTrace: {ex.StackTrace}");
        #    }
        #}
		return self.post(self.getPath(),self.formContent()) #??????????????????????????


    # <summary>
    # Form url for request
    # </summary>
    # <returns>url string.</returns>
	def getPath(self):
		return '%s/%s/%s' % (self._merchant.HOST, self._apiType, self.Command)

    # <summary>
    # Helper method for PaytureCommand.Init for form Redirect URL and save it in RedirectURL field for convinience
    # </summary>
    # <param name="response"></param>
    # <returns></returns>
	def formRedirectURL(self, response):
		sessionId = response.Attribute[PaytureParams.SessionId]
		response.RedirectURL = '%S/%s/%s?SessionId=%s' % (self._merchant.HOST, self._apiType, PaytureCommands.Add if _sessionType == SessionType.Add else PaytureCommands.Pay, sessionId)
		return response
