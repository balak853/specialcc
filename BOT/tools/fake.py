import httpx
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

FAKE_APIS = {
    "randomuser": "https://randomuser.me/api/?nat=",
    "namefake": "https://api.namefake.com/"
}

# Country Code Mapping
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
    "ae": "United Arab Emirates"
}

# Custom Fake Data for Some Countries
CUSTOM_FAKE_DATA = {
    "in": {
        "names": ["Rahul Sharma", "Priya Patel", "Amit Verma", "Sneha Iyer", "Vikram Gupta"],
        "cities": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"],
        "states": ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal"],
        "streets": ["MG Road", "Lajpat Nagar", "Brigade Road", "Anna Salai", "Park Street"],
        "phones": ["+91 9876543210", "+91 8765432109", "+91 7654321098"]
    },
    "us": {
        "names": ["John Smith", "Emma Johnson", "Michael Brown", "Emily Davis", "Chris Wilson"],
        "cities": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"],
        "states": ["New York", "California", "Illinois", "Texas", "Florida"],
        "streets": ["Main St", "Broadway", "Sunset Blvd", "Hollywood Blvd", "Elm Street"],
        "phones": ["+1 202-555-0143", "+1 312-555-0178", "+1 415-555-0199"]
    }
}

async def fetch_fake_data_from_api(country_code):
    country_name = COUNTRY_MAP.get(country_code.lower(), country_code.upper())

    # Use predefined fake data for specific countries
    if country_code in CUSTOM_FAKE_DATA:
        fake = CUSTOM_FAKE_DATA[country_code]
        return {
            "name": random.choice(fake["names"]),
            "gender": random.choice(["Male", "Female"]),
            "street": f"{random.randint(100, 9999)} {random.choice(fake['streets'])}",
            "city": random.choice(fake["cities"]),
            "state": random.choice(fake["states"]),
            "zipcode": str(random.randint(10000, 99999)),
            "phone": random.choice(fake["phones"]),
            "country": country_name
        }

    # Otherwise, fetch from APIs
    async def fetch(api_url):
        try:
            if "randomuser" in api_url:
                api_url += country_code  # Append country code for specific data
            
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
    return None  # If all fail

def parse_fake_data(api_url, data, country_name):
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
                "country": country_name
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
                "country": country_name
            }
    except Exception:
        return None
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
<b>Fake Info Created Successfully</b>
✅
───────────────
🆔 <b>Full Name</b> ➜ {fake_data['name']}
👤 <b>Gender</b> ➜ {fake_data['gender']}
🏡 <b>Street</b> ➜ {fake_data['street']}
🏙️ <b>City/Town/Village</b> ➜ {fake_data['city']}
🌍 <b>State/Province/Region</b> ➜ {fake_data['state']}
📮 <b>Postal Code</b> ➜ {fake_data['zipcode']}
📞 <b>Phone Number</b> ➜ {fake_data['phone']}
🌏 <b>Country</b> ➜ {fake_data['country']}
───────────────
<b>Checked By</b> ➜ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
"""
        await message.reply_text(resp)
    except Exception as e:
        import traceback
        await message.reply_text(f"Error: {traceback.format_exc()}")
