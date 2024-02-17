import requests
def dict_to_query(input_dict):
    '''
    (dict)-> str
    takes a dictionary as input, and returns a string containing the keys
    and values of the dictionary with the format 'key=value', and ampersands ('&') separating each.
    >>> dict_to_query({'email': 'jeffrey.nahas@mail.mcgill.ca', 'token': 'ABC'})

    'email=jeffrey.nahas@mail.mcgill.ca&token=ABC'
    >>> dict_to_query({'withdrawal_email': 'jeffrey.nahas@mail.mcgill.ca', 'token': 'ABC', 'amount': 25 , 'deposit_email': 'jonathan.campbell@mcgill.ca'})

    'withdrawal_email=jeffrey.nahas@mail.mcgill.ca&token=ABC&amount=25&deposit_email=jonathan.campbell@mcgill.ca'
    >>> dict_to_query({'withdrawal_email': 'jeffrey.nahas@mail.mcgill.ca'})
    'withdrawal_email=jeffrey.nahas@mail.mcgill.ca'
    '''
    list_query=[]
    for key in input_dict:
        value= str(input_dict[key])
        result= key + '=' + value
        list_query.append(result)
    new_str= '&'.join(list_query)
    return new_str

class Account:
    API_URL= 'https://coinsbot202.herokuapp.com/api/'
    
    def __init__(self,email,token):
        '''
        (str,str)-> Nonetype
        A constructor that takes an email (string) and token (string) as input. Raise an AssertionError
        if the types of the inputs are incorrect or if the email does not end in 'mcgill.ca'. Creates the
        following instance attributes: email: set to the input of the same name, token: set to the input of the same name, balance: set to -1,  request_log: set to an empty list
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "ABC")
        >>> my_acct.balance
        -1
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "ABC")
        >>> my_acct.email
        'jeffrey.nahas@mail.mcgill.ca'
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "abcedfg")
        >>> my_acct.token
        'abcdefg'
        '''
        if type(email)!= str or type(token)!= str or email[-9:]!= 'mcgill.ca':
            raise AssertionError("The types of the inputs are incorrect")
        self.balance=-1
        self.request_log=[]
        self.email= email
        self.token= token
        
    def __str__(self):
        '''
        ()-> str
        takes no input and  returns a string of the format 'EMAIL has balance BALANCE' where
        EMAIL and BALANCE refer to the appropriate instance attributes.
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "ABC")
        >>> print(my_acct)
        jeffrey.nahas@mail.mcgill.ca has balance -1
        '''
        return self.email + ' has balance '+ str(self.balance)
    
    def call_api(self, endpoint, ex_dict):
        '''
        (str,dict)-> dict
        takes an endpoint (string) and request dictionary as explicit inputs. If the types of the inputs are incorrect or the endpoint is not valid, raise an
        AssertionError. The method should add the key 'token' into the dictionary with value given
        by the instance attribute of the same name. It should then construct an API request URL and
        send the request as indicated on the previous page. If the 'status' in the result dictionary
        is not 'OK', raise an AssertionError with the value for the 'message' key as error message.
        Otherwise, return the result dictionary.
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "ABC")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.call_api("balance", {'email': my_acct.email})
        {'message': 98, 'status': 'OK'}
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.call_api("retrieve", {'email': my_acct.email})
        Traceback (most recent call last):
        AssertionError: The types of the inputs are incorrect
        '''
        if type(endpoint)!= str or type(ex_dict)!= dict or endpoint not in ('balance','transfer'):
            raise AssertionError("The types of the inputs are incorrect")
        ex_dict['token']= self.token
        request_url= self.API_URL + endpoint +'?'+ dict_to_query(ex_dict)
        result_dict = requests.get(url=request_url).json()
        self.request_log.append(result_dict)
        if result_dict['status'] != 'OK':
            raise AssertionError(result_dict['message'])
        return result_dict
    
    def retrieve_balance(self):
        '''
        ()-> int
        takes no explicit inputs. Calls the API to retrieve
        the balance for the current user email. Updates the balance attribute of the current user to
        the given value (after converting to integer), and returns the integer.
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.retrieve_balance()
        98
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "ABC")
        >>> my_acct.retrieve_balance()
        Traceback (most recent call last):
        AssertionError: The token in the API request did not match the token that was sent over Slack.
        '''
        result_dict= self.call_api('balance', {'email': self.email})
        new_balance = int(result_dict['message'])
        self.balance= new_balance
        return self.balance
    
    def transfer(self, amount_coins, user_email):
        '''
        (int,str)-> str
        takes a positive integer amount of coins and an email
        (string) for the user to which the coins should be transferred as explicit inputs. Raises an
        AssertionError if the types of the inputs are incorrect, if the given email does not end in
        'mcgill.ca', if the given email is equal to the current user’s email, if the current user’s balance
        is -1, if the given amount of coins is not positive or if the given amount of coins is greater than
        the user’s current balance. Calls the API to transfer the given amount to coins from the current
        user to the specified user. Returns the value for the key 'message' in the result dictionary.
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.retrieve_balance()
        98
        >>> my_acct.transfer(25, "mark.maroun@mail.mcgill.ca")
        'You have transferred 25 coins of your balance of 98 coins to mark.maroun. Your balance is now 73.'
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.transfer(100000, "mark.maroun@mail.mcgill.ca")
        Traceback (most recent call last):
        AssertionError: The amount of coins is not in bound
        >>> my_acct = Account("jeffrey.nahas@mail.mcgill.ca", "8p6k425cQPfR7gKb")
        >>> my_acct.transfer(25, "jeffrey.nahas@mail.mcgill.ca")
        Traceback (most recent call last):
        AssertionError: This is not a valid email adress
        '''
        if type(amount_coins)!= int or type(user_email)!= str:
            raise AssertionError("The types of the inputs are incorrect")
        if user_email[-9:]!= 'mcgill.ca' or user_email == self.email:
            raise AssertionError("This is not a valid email adress")
        if self.balance==-1:
            raise AssertionError("Not enough funds to be transfered")
        if amount_coins<0 or amount_coins > self.balance:
            raise AssertionError("The amount of coins is not in bound")
        result_dict= self.call_api('transfer', {'withdrawal_email': self.email, 'deposit_email': user_email, 'amount': amount_coins})
        return result_dict['message']
       
        
    
        
        
    
        
