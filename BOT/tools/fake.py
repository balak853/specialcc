import httpx
import random
from pyrogram import Client, filters
from bs4 import BeautifulSoup
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

# List of public APIs for generating fake information
FAKE_APIS = [
    "https://randomuser.me/api/",
    "https://fakerapi.it/api/v1/persons",
    "https://api.namefake.com/"
]

async def fetch_fake_data_from_api(country_code):
    for api_url in FAKE_APIS:
        try:
            async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:
                response = await client.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    return parse_fake_data(api_url, data, country_code)
        except Exception as e:
            continue  # If an API fails, try the next one
    return None  # If all APIs fail, return None


def parse_fake_data(api_url, data, country_code):
    if "randomuser.me" in api_url:
        user = data["results"][0]
        return {
            "name": f"{user['name']['first']} {user['name']['last']}",
            "gender": user["gender"].title(),
            "street": f"{user['location']['street']['number']} {user['location']['street']['name']}",
            "city": user["location"]["city"],
            "state": user["location"]["state"],
            "zipcode": user["location"]["postcode"],
            "phone": user["phone"],
            "country": user["location"]["country"]
        }
    elif "fakerapi.it" in api_url:
        user = random.choice(data["data"])
        return {
            "name": f"{user['firstname']} {user['lastname']}",
            "gender": "N/A",
            "street": "N/A",
            "city": user["city"],
            "state": "N/A",
            "zipcode": user["zipcode"],
            "phone": user["phone"],
            "country": country_code.upper()
        }
    elif "namefake.com" in api_url:
        return {
            "name": data["name"],
            "gender": data["gender"].title(),
            "street": data["address"],
            "city": data["city"],
            "state": data["state"],
            "zipcode": data["zip"],
            "phone": data["phone_h"],
            "country": country_code.upper()
        }
    return None


@Client.on_message(filters.command("fake", [".", "/"]))
async def cmd_fake(Client, message):
    try:
        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        country_code = message.text.split(" ")[1].lower() if len(message.text.split(" ")) > 1 else "us"
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
