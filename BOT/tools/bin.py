import csv
import pycountry
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

import pandas as pd  # Using Pandas for faster CSV lookup

# Load BIN data once into memory for faster access
BIN_DATA = pd.read_csv('FILES/bins_all.csv', dtype=str).set_index('bin', drop=False)

def get_bin_info_from_csv(fbin):
    try:
        if fbin in BIN_DATA.index:
            row = BIN_DATA.loc[fbin]
            return {
                "bin": row["bin"], "country": row["country"], "flag": row["flag"],
                "brand": row["brand"], "type": row["type"], "level": row["level"],
                "bank": row["bank"], "currency": row.get("currency", "N/A")
            }
    except Exception as e:
        print(f"Error fetching BIN info: {e}")
    return None

def get_country_name(code, fallback_country_name):
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else fallback_country_name
    except Exception as e:
        print(f"Country Lookup Error: {e}")
        return fallback_country_name

async def singlebinget(message):
    try:
        parts = message.text.split()
        return (parts[1], None, None, None) if len(parts) >= 2 else False
    except Exception:
        return False

@Client.on_message(filters.command("bin", [".", "/"]))
async def cmd_bin(client, message):
    try:
        checkall = await check_all_thing(client, message)
        if not checkall[0]: return

        bin = await singlebinget(message)
        if not bin:
            bin = await getmessage(message)
            if not bin:
                await message.reply_text("𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 𝐰𝐚𝐬 𝐟𝐨𝐮𝐧𝐝.", quote=True)
                return

        fbin = bin[0][:6] if bin and bin[0] else None
        if not fbin:
            await message.reply_text("𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐂𝐨𝐮𝐥𝐝 𝐧𝐨𝐭 𝐞𝐱𝐭𝐫𝐚𝐜𝐭 𝐁𝐈𝐍.", quote=True)
            return

        bin_info = get_bin_info_from_csv(fbin)
        if not bin_info:
            await message.reply_text("𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ⚠️\n\n𝐌𝐞𝐬𝐬𝐚𝐠𝐞: 𝐍𝐨 𝐁𝐈𝐍 𝐢𝐧𝐟𝐨 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞.", quote=True)
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
𝗜𝗻𝗳𝗼 ➜ <code>{brand} | {card_type} | {level}</code>  
𝗜𝘀𝘀𝘂𝗲𝗿 ➜ <code>{bank}</code>  
𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ➜ <code>{country_full_name}</code>  
𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆 ➜ <code>{currency}</code>  

━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━  
𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ <code>{message.from_user.first_name}</code>  
"""
        
        await message.reply_text(resp, quote=True)
    except Exception:
        import traceback
        await error_log(traceback.format_exc())
