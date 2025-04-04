import httpx
import asyncio
import random
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

FAKE_APIS = {
    "randomuser": "https://randomuser.me/api/?nat=",
    "namefake": "https://api.namefake.com/"
}

# Country-Specific Fake Data Enhancements
COUNTRY_DATA = {
    "in": {  # 🇮🇳 India
        "names": ["Amit Kumar", "Priya Sharma", "Rajesh Verma", "Suman Gupta", "Ravi Mehta", "Neha Joshi"],
        "streets": ["Bhavani Peth", "Lajpat Nagar", "Rajendra Place", "Sarojini Market", "Bandra West"],
        "cities": ["Mumbai", "Delhi", "Kolkata", "Chennai", "Bangalore", "Hyderabad"],
        "states": ["Maharashtra", "Delhi", "West Bengal", "Tamil Nadu", "Karnataka", "Telangana"],
        "phone_prefix": "+91",
        "country": "India"
    },
    "us": {  # 🇺🇸 USA
        "names": ["John Smith", "Emily Johnson", "Michael Brown", "Sarah Wilson", "David Jones"],
        "streets": ["Broadway", "Fifth Avenue", "Sunset Boulevard", "Maple Street"],
        "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "states": ["New York", "California", "Illinois", "Texas", "Arizona"],
        "phone_prefix": "+1",
        "country": "United States"
    },
    "uk": {  # 🇬🇧 United Kingdom
        "names": ["Oliver Smith", "Amelia Jones", "Harry Brown", "Sophia Wilson", "Jack Taylor"],
        "streets": ["Baker Street", "Oxford Street", "King’s Road", "Piccadilly"],
        "cities": ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool"],
        "states": ["England", "Scotland", "Wales", "Northern Ireland"],
        "phone_prefix": "+44",
        "country": "United Kingdom"
    },
    "ca": {  # 🇨🇦 Canada
        "names": ["Liam Martin", "Charlotte Anderson", "Noah Thomas", "Ava White", "Mason Harris"],
        "streets": ["Bay Street", "Queen Street", "Robson Street", "Yonge Street"],
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "states": ["Ontario", "British Columbia", "Quebec", "Alberta", "Manitoba"],
        "phone_prefix": "+1",
        "country": "Canada"
    },
    "default": {  # Default if country code not found
        "names": ["Alex Doe", "Chris Johnson", "Jordan Lee", "Taylor White"],
        "streets": ["Elm Street", "Main Street", "Cedar Avenue", "Pine Road"],
        "cities": ["Springfield", "Riverside", "Greenwood", "Fairview"],
        "states": ["State A", "State B", "State C"],
        "phone_prefix": "+99",
        "country": "Unknown"
    }
}

async def fetch_fake_data(country_code):
    country_code = country_code.lower()
    country_data = COUNTRY_DATA.get(country_code, COUNTRY_DATA["default"])

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
            parsed_data = parse_fake_data(api_url, data, country_data)
            if parsed_data:
                return parsed_data

    return generate_fallback_data(country_data)

def parse_fake_data(api_url, data, country_data):
    try:
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
                "country": country_data["country"]
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
                "country": country_data["country"]
            }
    except Exception:
        return None
    return None

def generate_fallback_data(country_data):
    return {
        "name": random.choice(country_data["names"]),
        "gender": random.choice(["Male", "Female"]),
        "street": f"{random.randint(1, 9999)} {random.choice(country_data['streets'])}",
        "city": random.choice(country_data["cities"]),
        "state": random.choice(country_data["states"]),
        "zipcode": random.randint(10000, 99999),
        "phone": f"{country_data['phone_prefix']} {random.randint(6000000000, 9999999999)}",
        "country": country_data["country"],
    }

@Client.on_message(filters.command("fake", [".", "/"]))
async def cmd_fake(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        args = message.text.split(" ")
        country_code = args[1].lower() if len(args) > 1 else "us"

        fake_data = await fetch_fake_data(country_code)
        if not fake_data:
            await message.reply_text("❌ Failed to fetch fake data. Try again later.")
            return

        resp = f"""
<b>✅ Fake Info Created Successfully</b>
━━━━━━━━━━━━━━━━━━━━━━
🆔 <b>Full Name:</b> <code>{fake_data['name']}</code>
👤 <b>Gender:</b> <code>{fake_data['gender']}</code>
🏠 <b>Street:</b> <code>{fake_data['street']}</code>
🏙️ <b>City/Town/Village:</b> <code>{fake_data['city']}</code>
🌍 <b>State/Province/Region:</b> <code>{fake_data['state']}</code>
📮 <b>Postal Code:</b> <code>{fake_data['zipcode']}</code>
📞 <b>Phone Number:</b> <code>{fake_data['phone']}</code>
🌏 <b>Country:</b> <code>{fake_data['country']}</code>
━━━━━━━━━━━━━━━━━━━━━━
<b>Checked By:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
"""
        await message.reply_text(resp)
    except Exception as e:
        import traceback
        await message.reply_text(f"Error: {traceback.format_exc()}")
