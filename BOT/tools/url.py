import httpx
from pyrogram import Client, filters
from bs4 import BeautifulSoup
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

# List of public APIs
PUBLIC_APIS = [
    "https://api.urlscan.io/v1/search/?q=domain:{}",
    "https://ipwhois.app/json/{}"
]

def fetch_data(website):
    """Fetches data from multiple public APIs and returns the first valid response."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for api in PUBLIC_APIS:
        try:
            url = api.format(website)
            with httpx.Client(headers=headers, timeout=10) as client:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        return data  # Return if valid data found
        except Exception as e:
            print(f"⚠️ API request failed: {api} | Error: {e}")

    return None  # Return None if no data is found

@Client.on_message(filters.command("url", [".", "/"]))
async def cmd_url(client, message):
    """Handles the /url command to fetch website details from public APIs."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("❌ Usage: /url <website_url>")
        return
    
    website = args[1].strip()

    if not website.startswith(("http://", "https://")):
        await message.reply_text("❌ Invalid URL. Please enter a valid website URL (e.g., https://example.com).")
        return

    # ⏳ Send processing message
    processing_msg = await message.reply_text("🔄 Fetching data, please wait...")

    # Fetch data
    data = fetch_data(website)

    # Delete processing message
    await processing_msg.delete()

    if not data:
        await message.reply_text("❌ No data found from any public API.")
        return

    # Extract relevant data safely
    result = f"""
🔍 *Gateways Fetched Successfully ✅*
━━━━━━━━━━━━━
🚀 *URL:* `{website}`
🚀 *Payment Gateways:* `{data.get('payment_gateways', 'N/A')}`
🚀 *Captcha:* `{data.get('security', {}).get('captcha', 'False')}`
🚀 *Cloudflare:* `{data.get('protection', {}).get('cloudflare', 'False')}`
🚀 *GraphQL:* `{data.get('technology', {}).get('graphql', 'False')}`
🚀 *Platform:* `{data.get('technology', {}).get('platform', 'N/A')}`
🚀 *Error Logs:* `{data.get('logs', {}).get('error', 'N/A')}`
🚀 *Status:* `{data.get('status', 'Unknown')}`

👤 *Checked By:* [{message.from_user.first_name}](tg://user?id={message.from_user.id})  
🤖 *Bot by:* [【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎](tg://user?id=7028548502)
"""

    # Send final result (This message will NOT be deleted)
    await message.reply_text(result, parse_mode="Markdown")
