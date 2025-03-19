import httpx
import re
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *
import asyncio
import json
import httpx
import Application, CommandHandler
from bs4 import BeautifulSoup
import cloudscraper


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I'm a gateway lookup bot! Use /url <website_url> to get information."
    )

async def url_lookup(update, context):
    if len(context.args) != 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Please provide a valid URL. Example: /url https://www.example.com"
        )
        return

    url = context.args[0]
    try:
        processing_message = await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Processing your site..."
        )
        
        result = await get_website_info(url)
        message = (f"🔍 Gateways Fetched Successfully ✅\n━━━━━━━━━━━━━\n"
                   f"🚀 URL: {result['url']}\n"
                   f"🚀 Payment Gateways: {result['payment_gateways']}\n"
                   f"🚀 Captcha: {result['captcha']}\n"
                   f"🚀 Cloudflare: {result['cloudflare']}\n"
                   f"🚀 GraphQL: {result['graphql']}\n"
                   f"🚀 Platform: {result['platform']}\n"
                   f"🚀 Error Logs: {result['error_logs']}\n"
                   f"🚀 Status: {result['status']}\n\n"
                   "🤖 Bot by: BADNAAM")
        
        # Replace values for better readability
        message = (message.replace("Yes", "True 🙂")
                         .replace("No", "False 🔥")
                         .replace("Possible errors detected", "True 🙂")
                         .replace("None detected", "False 🔥")
                         .replace("Error", "False 🔥")
                         .replace("Not detected", "False 🔥"))

        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, 
            message_id=processing_message.message_id, 
            text=message
        )
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, 
            message_id=processing_message.message_id, 
            text=f"An error occurred: {e}"
        )

async def get_website_info(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        payment_gateways = detect_payment_gateways(soup)
        captcha = detect_captcha(soup)
        cloudflare = detect_cloudflare(response)
        graphql = await detect_graphql(url)
        platform = detect_platform(soup)
        error_logs = detect_error_logs(response.text)
        status = response.status_code

        return {
            'url': url,
            'payment_gateways': ', '.join(payment_gateways) if payment_gateways else 'False 🔥',
            'captcha': captcha,
            'cloudflare': cloudflare,
            'graphql': graphql,
            'platform': platform,
            'error_logs': error_logs,
            'status': status
        }
    except httpx.RequestError as e:
        return {
            'url': url,
            'payment_gateways': 'False 🔥',
            'captcha': 'False 🔥',
            'cloudflare': 'False 🔥',
            'graphql': 'False 🔥',
            'platform': 'False 🔥',
            'error_logs': str(e),
            'status': 'False 🔥'
        }

def detect_payment_gateways(soup):
    gateways = []
    if soup.find(string=re.compile(r'stripe', re.IGNORECASE)):
        gateways.append("Stripe")
    if soup.find(string=re.compile(r'paypal', re.IGNORECASE)):
        gateways.append("PayPal")
    if soup.find(string=re.compile(r'razorpay', re.IGNORECASE)):
        gateways.append("Razorpay")
    return gateways

def detect_captcha(soup):
    if soup.find('div', {'class': 'g-recaptcha'}) or soup.find('iframe', {'src': re.compile(r'google\.com/recaptcha')}):
        return "reCAPTCHA"
    elif soup.find('input', {'name': 'h-captcha-response'}):
        return "hCaptcha"
    return "False 🔥"

def detect_cloudflare(response):
    if 'cloudflare' in response.headers.get('Server', '').lower() or 'cf-ray' in response.headers:
        return "True 🙂"
    return "False 🔥"

async def detect_graphql(url):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(f"{url}/graphql", json={"query": "{ __schema { types { name } } }"})
        if response.status_code == 200 and "data" in response.json():
            return "True 🙂"
    except Exception:
        pass
    return "False 🔥"

def detect_platform(soup):
    if soup.find('meta', {'name': 'generator'}):
        return soup.find('meta', {'name': 'generator'})['content']
    if soup.find('link', {'rel': 'stylesheet', 'href': re.compile(r'/wp-content/')}):
        return "WordPress"
    if soup.find('link', {'rel': 'stylesheet', 'href': re.compile(r'/skin/frontend/')}):
        return "Magento"
    return "Unknown"

def detect_error_logs(text):
    return "True 🙂" if re.search(r'error|exception|warning', text, re.IGNORECASE) else "False 🔥
