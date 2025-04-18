import csv
import pycountry
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *
import re  # Regex for extracting first 6 digits

async def singlebinget(message):
    try:
        parts = message.text.split()
        return parts[1] if len(parts) >= 2 else False
    except Exception as e:
        print(f"Error in singlebinget: {e}")
        return False

def get_bin_info_from_csv(fbin, csv_file='FILES/bins_all.csv'):
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == fbin:
                    return {
                        "bin": row[0],
                        "country": row[1],
                        "flag": row[2],
                        "brand": row[3],
                        "type": row[4],
                        "level": row[5],
                        "bank": row[6],
                        "currency": row[7] if len(row) > 7 and row[7].strip() else "N/A"
                    }
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return {}

def get_country_name(code, fallback_country_name):
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else fallback_country_name
    except Exception as e:
        print(f"Error getting country name: {e}")
        return fallback_country_name

@Client.on_message(filters.command("bin", [".", "/"]))
async def cmd_bin(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]  # Correctly assigned role from user check

        bin_number = await singlebinget(message)

        # Agar user reply message me command use kare toh reply message se BIN extract kare
        if not bin_number and message.reply_to_message:
            reply_text = message.reply_to_message.text.strip()
            match = re.search(r'\d{6,}', reply_text)  # Extract first 6+ digit number
            if match:
                bin_number = match.group()[:6]  # Take first 6 digits only

        if not bin_number:
            bin_number = await getmessage(message)

        if not bin_number or len(bin_number) < 6:
            resp = """
𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️

𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐕𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 𝐰𝐚𝐬 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐢𝐧𝐩𝐮𝐭.
"""
            await message.reply_text(resp, quote=True)
            return

        fbin = bin_number[:6]
        bin_info = get_bin_info_from_csv(fbin)

        if not bin_info:
            resp = """
𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️

𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐕𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐭𝐡𝐞 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞.
"""
            await message.reply_text(resp, quote=True)
            return

        brand = bin_info.get("brand", "N/A").upper()
        card_type = bin_info.get("type", "N/A").upper()
        level = bin_info.get("level", "N/A").upper()
        bank = bin_info.get("bank", "N/A").upper()
        country_code = bin_info.get("country", "N/A").upper()
        flag = bin_info.get("flag", "")
        currency = bin_info.get("currency", "N/A").upper()
        country_full_name = get_country_name(country_code, country_code)

        resp = f"""
𝐁𝐢𝐧 𝐋𝐨𝐨𝐤𝐮𝐩 𝐑𝐞𝐬𝐮𝐥𝐭 🔍
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
𝐁𝐢𝐧 ➜ <code>{fbin}</code> 
𝗜𝗻𝗳𝗼 ➜ <code>{brand}-{card_type}-{level}</code> 
𝗜𝘀𝘀𝘂𝗲𝗿 ➜ <code>{bank} 🏛</code> 
𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ➜ <code>{country_full_name} {flag}</code> 
𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆 ➜ <code>{currency}</code>
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ 
<b>𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ⤿ {role} ⤾
━━━━━━━━━━━━━━━"""
        await message.reply_text(resp, quote=True)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
