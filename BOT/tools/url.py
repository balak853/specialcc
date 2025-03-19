import httpx
import re
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

# List of public APIs
PUBLIC_APIS = [
    "https://api.urlscan.io/v1/search/?q=domain:{}",
    "https://ipwhois.app/json/{}"
]

def extract_domain(url):
    """Extracts the domain name from a given URL."""
    match = re.search(r"https?://([^/]+)", url)
    return match.group(1) if match else url

def fetch_data(website):
    """Fetches data from multiple public APIs and returns the first valid response."""
    headers = {"User-Agent": "Mozilla/5.0"}
    domain = extract_domain(website)  # Ensure we're passing just the domain

    for api in PUBLIC_APIS:
        try:
            url = api.format(domain)
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

    if not re.match(r"https?://", website):
        await message.reply_text("❌ Invalid URL. Please enter a valid website URL (e.g., https://example.com).")
        return

    # Show processing message
    processing_msg = await message.reply_text("🔄 *Processing...*\n_Please wait while we fetch data..._", parse_mode="Markdown")

    # Fetch data
    data = fetch_data(website)

    if not data:
        await processing_msg.edit_text("❌ No data found from any public API.")
        return

    # Extract relevant data safely
    payment_gateways = data.get("payment_gateways", "N/A")
    security = data.get("security") or {}  # Ensures security key exists
    protection = data.get("protection") or {}
    technology = data.get("technology") or {}
    logs = data.get("logs") or {}

    result = f"""
🔍 *Gateways Fetched Successfully ✅*
━━━━━━━━━━━━━
🚀 *URL:* `{website}`
🚀 *Payment Gateways:* `{payment_gateways}`
🚀 *Captcha:* `{security.get('captcha', 'False')}`
🚀 *Cloudflare:* `{protection.get('cloudflare', 'False')}`
🚀 *GraphQL:* `{technology.get('graphql', 'False')}`
🚀 *Platform:* `{technology.get('platform', 'N/A')}`
🚀 *Error Logs:* `{logs.get('error', 'N/A')}`
🚀 *Status:* `{data.get('status', 'Unknown')}`

👤 *Checked By:* [{message.from_user.first_name}](tg://user?id={message.from_user.id})  
🤖 *Bot by:* [【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎](tg://user?id=7028548502)
"""

    # Update the processing message with final data
    await processing_msg.edit_text(result, parse_mode="Markdown")
