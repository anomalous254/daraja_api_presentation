import base64
import json
import requests
from datetime import datetime



class DarajaAPI:
    def __init__(self, url: str,consumer_key: str,  consumer_secret :str, passkey:str, shortcode:str , phone_number:str):
        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.passkey =passkey
        self.shortcode = shortcode
        self.phone_number = phone_number

    def __generate_access_token(self):
      
        try:
            
            encoded_credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()

            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/json"
            }

            # Send the request and parse the response
            response = requests.get(self.url, headers=headers).json()

            # Check for errors and return the access token
            if "access_token" in response:
                return response["access_token"]
            else:
                raise Exception("Failed to get access token: " + response["error_description"])
        except Exception as e:
            raise Exception("Failed to get access token: " + str(e)) 
        
       
    def send_stk_push(self, url : str):
        token = self.__generate_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        """ shortCode = "YOUR_PAYBILL" #sandbox -174379
        passkey = "YOUR_PASSKEY" """
        stk_password = base64.b64encode((self.shortcode + self.passkey + timestamp).encode('utf-8')).decode('utf-8')
        
      

        
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        
        requestBody = {
            "BusinessShortCode": self.shortcode,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline", #till "CustomerBuyGoodsOnline"
            "Amount": "1",
            "PartyA":  self.phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber":  self.phone_number,
            "CallBackURL": "", #Your callback url goes here 
            "AccountReference":  self.shortcode,
            "TransactionDesc": "test"
        }
        
        try:
            response = requests.post(url, json=requestBody, headers=headers)
            return response.json()
        except Exception as e:
            print('Error:', str(e))



