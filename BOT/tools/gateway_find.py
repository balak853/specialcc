import re
from pyrogram import Client, filters
import requests
import time

# Import your specific functionalities
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *
from FUNC.defs import *

GROUP_CHAT_ID = '-1002282387595' 
MAX_URLS = 20  # Maximum number of URLs allowed

@Client.on_message(filters.command("url", prefixes=[".", "/"]))
async def analyze_url_and_forward(client, message):
    try:
        user_input = message.text.split(maxsplit=1)
        
        if len(user_input) < 2:
            await message.reply_text("No URL provided. Please provide a URL after the command.", quote=True)
            return
        
        urls = user_input[1].strip().split()  # Split the input into URLs

        if len(urls) > MAX_URLS:
            await message.reply_text(f"Maximum limit of {MAX_URLS} URL(s) exceeded. Please provide only {MAX_URLS} URL(s).", quote=True)
            return

        for url in urls:
            # Ensure URL has a scheme
            if not re.match(r'^https?://', url):
                url = 'https://' + url
            
            checking_msg = await message.reply_text('Processing your site...')
            
            result = analyze_site(url)
            formatted_result = format_result(result)
            
            await client.edit_message_text(message.chat.id, checking_msg.id, formatted_result)
            
            if not result['captcha']:
                await client.send_message(GROUP_CHAT_ID, formatted_result)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())

def format_result(result):
    captcha_status = "True 🙂" if result['captcha'] else "False 🔥"
    cloudflare_status = "True 🙂" if result['cloudflare'] else "False 🔥"
    
    formatted_result = (
        f"🔍 Gateways Fetched Successfully ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"🚀 URL: <code>{result['url']}</code>\n"
        f"🚀 Payment Gateways: <code>{', '.join(result['payment_gateways']) if result['payment_gateways'] else 'None'}</code>\n"
        f"🚀 Captcha: <code>{captcha_status}</code>\n"
        f"🚀 Cloudflare: <code>{cloudflare_status}</code>\n"
        f"🚀 GraphQL: <code>{result['graphql']}</code>\n"
        f"🚀 Platform: <code>{result['platform'] if result['platform'] else 'None'}</code>\n"
        f"🚀 Error Logs: <code>{result['error'] if result['error'] else 'None'}</code>\n"
        f"🚀 Status: <code>{result['http_status']}</code>\n\n"
        f"🤖 Bot by: <a href=\"tg://user?id=7113416108\">н ɪ ✟ ʟ є я</a>\n"
    )
    return formatted_result

def analyze_site(url):
    result = {'url': url, 'payment_gateways': [], 'captcha': False, 'cloudflare': False,
              'graphql': False, 'platform': None, 'http_status': None, 'error': None}
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        headers = response.headers
        cookies = response.cookies
        content_type = headers.get('Content-Type', '')

        # Payment Gateway checks
        result['payment_gateways'] = check_for_payment_gateway(headers, content_type, cookies, html)

        # Cloudflare detection
        result['cloudflare'] = check_for_cloudflare(response.text)

        # CAPTCHA detection
        result['captcha'] = check_for_captcha(response.text)

        # Additional checks based on content type, cookies, etc.
        result['content_type'] = content_type
        result['cookies'] = cookies.get_dict()

        # GraphQL detection
        result['graphql'] = check_for_graphql(response.text)

        # Platform detection
        result['platform'] = check_for_platform(response.text)

        # HTTP status code
        result['http_status'] = response.status_code

    except requests.Timeout:
        result['error'] = 'Timeout error. Unable to fetch the page within the specified time.'
    except Exception as e:
        result['error'] = str(e)

    return result

def check_for_payment_gateway(headers, content_type, cookies, html):
    gateway_keywords = {
        'mollie': ['mollie', 'api.mollie.com', 'mollie.com', 'mollie-payment', 'mollie-checkout', 'mollie-form', 'mollie-sdk', 'mollie-subscription', 'mollie-token', 'mollie-merchant', 'mollie-billing', 'mollie-gateway'],
        'square': ['square', 'squareup.com', 'square-payment', 'square-checkout', 'square-form', 'square-sdk', 'square-subscription', 'square-token', 'square-merchant', 'square-billing', 'square-gateway','connect.squareup.com','connect.squareup.com/v2/analytics','connect.squareup.com/v2/analytics/verifications'],
        'cybersource': ['cybersource', 'cybersource.com', 'cybersource-payment', 'cybersource-checkout', 'cybersource-form', 'cybersource-sdk', 'cybersource-subscription', 'cybersource-token', 'cybersource-merchant', 'cybersource-billing', 'cybersource-gateway'],
        '2checkout': ['2checkout', '2checkout.com', '2checkout-payment', '2checkout-checkout', '2checkout-form', '2checkout-sdk', '2checkout-subscription', '2checkout-token', '2checkout-merchant', '2checkout-billing', '2checkout-gateway'],
        'eway': ['eway', 'eway.com', 'eway-payment', 'eway-checkout', 'eway-form', 'eway-sdk', 'eway-subscription', 'eway-token', 'eway-merchant', 'eway-billing', 'eway-gateway'],
        'stripe': ['stripe', 'checkout.stripe.com', 'js.stripe.com', 'stripe.com', 'stripe-elements', 'stripe-js-v3',
                   'stripe-button', 'stripe-payment', 'stripe-checkout', 'stripe-form', 'stripe-sdk', 'stripe-pay',
                   'stripe-card', 'stripe-subscription', 'stripe-checkout-button', 'stripe-elements', 'stripe-token'],
        'paypal': ['paypal', 'paypal.com', 'smart/buttons.js', 'checkout.js', 'paypal-checkout', 'paypal-button',
                   'paypal-payment', 'paypal-express', 'paypal-form', 'paypal-sdk', 'paypal-checkout-button',
                   'paypal-subscription', 'paypal-token', 'paypal-merchant', 'paypal-billing', 'paypal-braintree'],
        'braintree': ['https://js.braintreegateway.com/js/braintree-2.32.1.min.js','braintree', 'braintreegateway.com', 'braintree-api.com', 'data-braintree-name', 'braintree.js',
                      'braintree-payment', 'braintree-button', 'braintree-form', 'braintree-sdk', 'braintree-checkout',
                      'braintree-subscription', 'braintree-token', 'braintree-merchant', 'braintree-billing'],
        'worldpay': ['worldpay', 'worldpay.com', 'secure.worldpay.com', 'wp-e-commerce', 'worldpay-button',
                     'worldpay-payment', 'worldpay-express', 'worldpay-form', 'worldpay-sdk', 'worldpay-checkout',
                     'worldpay-subscription', 'worldpay-token', 'worldpay-merchant', 'worldpay-billing'],
        'authnet': ['authnet', 'authorize.net', 'authorizenet.com', 'accept-sdk', 'anet', 'authnet-button',
                    'authnet-payment', 'authnet-express', 'authnet-form', 'authnet-sdk', 'authnet-checkout',
                    'authnet-subscription', 'authnet-token', 'authnet-merchant', 'authnet-billing'],
        'recurly': ['recurly', 'recurly.com', 'recurly.js', 'recurly-integration', 'recurly-button', 'recurly-payment',
                    'recurly-checkout', 'recurly-form', 'recurly-sdk', 'recurly-express', 'recurly-subscription',
                    'recurly-token', 'recurly-merchant', 'recurly-billing'],
        'shopify': ['shopify', 'myshopify', 'shopify.com', 'checkout.shopify.com', 'shopify-checkout', 'shopify-payment-button',
                    'shopify-payment', 'shopify-checkout-button', 'shopify-express', 'shopify-form', 'shopify-sdk',
                    'shopify-subscription', 'shopify-token', 'shopify-merchant', 'shopify-billing'],
        'ayden': ['ayden', 'adyen', 'adyen.com', 'adyen-payment', 'adyen-express', 'adyen-form', 'adyen-sdk',
                  'adyen-checkout', 'adyen-subscription', 'adyen-token', 'adyen-merchant', 'adyen-billing'],
    }

    found_gateways = []

    for keyword, values in gateway_keywords.items():
        if (keyword in content_type.lower() or
                any(key.lower() in headers or key.lower() in html or keyword.lower() in str(cookies) for key in
                    values)):
            found_gateways.append(keyword.capitalize())

    return found_gateways

def check_for_cloudflare(response_text):
    cloudflare_markers = [
        'checking your browser', 'cf-ray', 'cloudflare',
        '__cfduid', '__cflb', '__cf_bm', 'cf_clearance'
    ]

    for marker in cloudflare_markers:
        if marker in response_text.lower():
            return True

    return False

def check_for_captcha(response_text):
    captcha_markers =[
        'recaptcha', 'g-recaptcha', 'data-sitekey',
        'captcha', 'cf_captcha', 'arkoselabs'
    ]

    for marker in captcha_markers:
        if marker in response_text.lower():
            return True

    return False

def check_for_graphql(response_text):
    graphql_markers = ['graphql', 'application/graphql']

    for marker in graphql_markers:
        if marker in response_text.lower():
            return True

    return False

def check_for_platform(response_text):
    platform_markers = {
        'woocommerce': ['woocommerce', 'wc-cart', 'wc-ajax'],
        'magento': ['magento', 'mageplaza'],
        'shopify': ['shopify', 'myshopify'],
        'prestashop': ['prestashop', 'addons.prestashop'],
        'opencart': ['opencart', 'route=common/home'],
        'bigcommerce': ['bigcommerce', 'stencil'],
        'wordpress': ['wordpress', 'wp-content'],
        'drupal': ['drupal', 'sites/all'],
        'joomla': ['joomla', 'index.php?option=com_']
    }

    for platform, markers in platform_markers.items():
        if any(marker in response_text.lower() for marker in markers):
            return platform.capitalize()

    return None
  
