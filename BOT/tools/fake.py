import httpx
import random
import asyncio
from pyrogram import Client, filters
from bs4 import BeautifulSoup
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

FAKE_APIS = {
    "randomuser": "https://randomuser.me/api/?nat=",
    "namefake": "https://api.namefake.com/"  # optional fallback
}

COUNTRY_MAP = {
    "us": "United States",
    "in": "India",
    "gb": "United Kingdom",
    "ca": "Canada",
    "au": "Australia",
    "de": "Germany",
    "fr": "France",
    "it": "Italy",
    "es": "Spain",
    "nl": "Netherlands",
    "br": "Brazil",
    "mx": "Mexico",
    "ru": "Russia",
    "jp": "Japan",
    "cn": "China",
    "kr": "South Korea",
    "za": "South Africa",
    "ae": "United Arab Emirates",
    "pk": "Pakistan",
    "bd": "Bangladesh",
    "ph": "Philippines",
    "id": "Indonesia"
}

async def fetch_fake_data_from_api(country_code):
    country_name = COUNTRY_MAP.get(country_code.lower(), country_code.upper())

    # Use realistic web-scraped data for specific countries
    if country_code.lower() in ["in", "br", "pk", "bd", "ph", "id"]:
        return await scrape_fakename_generator(country_name)

    async def fetch(api_url):
        try:
            if "randomuser" in api_url:
                api_url += country_code

            async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:
                response = await client.get(api_url)
                if response.status_code == 200:
                    return api_url, response.json()
        except Exception:
            return None, None

    tasks = [fetch(api) for api in FAKE_APIS.values()]
    results = await asyncio.gather(*tasks)

    for api_url, data in results:
        if data:
            parsed_data = parse_fake_data(api_url, data, country_name)
            if parsed_data:
                return parsed_data
    return None

def parse_fake_data(api_url, data, country_name):
    try:
        if "randomuser.me" in api_url:
            user = data["results"][0]
            return {
                "name": f"{user['name']['first']} {user['name']['last']}",
                "gender": user["gender"].title(),
                "street": f"{user['location']['street']['number']} {user['location']['street']['name']}",
                "city": user["location"].get("city", "Unknown"),
                "state": user["location"].get("state", "Unknown"),
                "zipcode": str(user["location"].get("postcode", "Unknown")),
                "phone": user.get("phone", "N/A"),
                "country": country_name
            }
        elif "namefake.com" in api_url:
            return {
                "name": data.get("name", "Unknown"),
                "gender": data.get("gender", "Unknown").title(),
                "street": data.get("address", "Unknown"),
                "city": data.get("city", "Unknown"),
                "state": data.get("state", "Unknown"),
                "zipcode": data.get("zip", "Unknown"),
                "phone": data.get("phone_h", "N/A"),
                "country": country_name
            }
    except Exception:
        return None
    return None

async def scrape_fakename_generator(country_name):
    try:
        async with httpx.AsyncClient() as client:
            url_country = country_name.lower().replace(" ", "-")
            url = f"https://www.fakenamegenerator.com/gen-random-{url_country}.php"
            response = await client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            name = soup.find("div", {"class": "address"}).h3.text.strip()
            address_block = soup.find("div", {"class": "address"}).find_all("div")[0].text.strip().split("\n")
            street = address_block[0].strip()
            city_state_zip = address_block[1].strip().split(",")
            city = city_state_zip[0].strip()
            state_zip = city_state_zip[1].strip().split(" ")
            state = " ".join(state_zip[:-1])
            zipcode = state_zip[-1]

            info_section = soup.find_all("dl")[1]
            dt_tags = info_section.find_all("dt")
            dd_tags = info_section.find_all("dd")
            info = {dt.text.strip(): dd.text.strip() for dt, dd in zip(dt_tags, dd_tags)}
            gender = info.get("Gender", "Unknown")
            phone = info.get("Phone", "N/A")

            return {
                "name": name,
                "gender": gender,
                "street": street,
                "city": city,
                "state": state,
                "zipcode": zipcode,
                "phone": phone,
                "country": country_name
            }
    except Exception:
        return None

@Client.on_message(filters.command("fake", [".", "/"]))
async def cmd_fake(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        args = message.text.split(" ")
        country_code = args[1].lower() if len(args) > 1 else "us"

        fake_data = await fetch_fake_data_from_api(country_code)
        if not fake_data:
            await message.reply_text("❌ Failed to fetch fake data. Try again later.")
            return

        resp = f"""
<b>Fake Info Created Successfully ✅</b>
━━━━━━━━━━━━━━
🆔 <b>Full Name:</b> <code>{fake_data['name']}</code>
👤 <b>Gender:</b> <code>{fake_data['gender']}</code>
🏠 <b>Street:</b> <code>{fake_data['street']}</code>
🏙️ <b>City/Town/Village:</b> <code>{fake_data['city']}</code>
🌍 <b>State/Province/Region:</b> <code>{fake_data['state']}</code>
📮 <b>Postal Code:</b> <code>{fake_data['zipcode']}</code>
📞 <b>Phone Number:</b> <code>{fake_data['phone']}</code>
🌏 <b>Country:</b> <code>{fake_data['country']}</code>
━━━━━━━━━━━━━━
<b>Checked By:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
<b>Bot by:</b> <a href="tg://user?id=7028548502">【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎</a>
"""
        await message.reply_text(resp)
    except Exception as e:
        import traceback
        await message.reply_text(f"Error: {traceback.format_exc()}")
