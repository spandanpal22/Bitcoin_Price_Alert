from boltiot import Sms,Email
import json,time
import bitcoin_conf as conf
from requests import request

#set your desirable limits
minimum_limit=4000 
maximum_limit=5000

sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECIPIENT_EMAIL)

def get_bitcoin_price():
    #here I am using only USD and INR you can add more by editing the URL here
    URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,INR"

    try:    
        response=request("GET",URL)
        print(response)
        response=json.loads(response.text)
        current_price={}
        current_price['USD']=response["USD"]
        current_price['INR']=response["INR"]
        return current_price        
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
            
while True:
    price=get_bitcoin_price()
    print("Bitcoin price in USD and INR is as follows :\n1. USD : "+str(price['USD'])+"\n2. INR : "+str(price['INR'])+"\n")
    try:
        if price['INR']>maximum_limit or price['INR']<minimum_limit:
            
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms("Bitcoin price has crossed your set limits.\nCurrent bitcoin price in USD is " +str(price['USD'])+" and in INR is "+str(price['INR']))
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
            

            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Bitcoin_Price_Alert", "Bitcoin price has crossed your set limits.\nCurrent bitcoin price in USD is " +str(price['USD'])+" and in INR is "+str(price['INR']))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))

    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10) #set the time you want to delay I have set it to 10sec
