import httpx
import time
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *

@Client.on_message(filters.command("vbv", [".", "/"]))
async def stripe_auth_cmd(Client, message):
    try:
        user_id = message.from_user.id
        gateway = "3DS Lookup"
        approve = "𝗣𝗮𝘀𝘀𝗲𝗱 ✅"

        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if not getcc:
            await message.reply_text("""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴... ❌
╚═══════════════════╝

❌ No CC Found in your input.
Usage: /vbv cc|mes|ano|cvv
""", message.id)
            return

        cc, mes, ano, cvv = getcc
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        bin = cc[:6]

        if bin.startswith('3'):
            await message.reply_text("""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴... ❌
╚═══════════════════╝

❌ Unsupported card type.
""", message.id)
            return
        
        checking_msg = await message.reply_text("""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴...
╚═══════════════════╝

🃏 𝗖𝗖 - <code>{fullcc}</code>
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - {gateway}
⚡ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□ 30%

🔑 𝗥𝗲𝗾: Processing...
""", message.id)
        
        await asyncio.sleep(1)
        await Client.edit_message_text(message.chat.id, checking_msg.id, f"""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴...
╚═══════════════════╝

🃏 𝗖𝗖 - <code>{fullcc}</code>
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - {gateway}
⚡ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■■■□ 70%

🔑 𝗥𝗲𝗾: Processing...
""")
        
        await asyncio.sleep(1)
        await Client.edit_message_text(message.chat.id, checking_msg.id, f"""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴...
╚═══════════════════╝

🃏 𝗖𝗖 - <code>{fullcc}</code>
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - {gateway}
⚡ 𝐑𝐞𝐬𝗽𝗼𝗻𝘀𝗲 - ■■■■ 99%

🔑 𝗥𝗲𝗾: Processing...
""")

        # Check vbvbin.txt file more efficiently
        bin_found, bin_response, response_message = False, "Not Found", "Lookup Card Error"
        try:
            with open("FILES/vbvbin.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith(bin):
                        bin_found = True
                        parts = line.strip().split('|')
                        bin_response = parts[1]
                        response_message = parts[2]
                        if "3D TRUE ❌" in bin_response:
                            approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
                        break
        except FileNotFoundError:
            response_message = "Error: vbvbin.txt not found"
        
        if not bin_found:
            approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"

        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=100) as session:
            getbin = await get_bin_details(cc)

        brand, type, level, bank, country, flag = getbin

        finalresp = f"""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴... ✅
╚═══════════════════╝

🃏 𝗖𝗖 - <code>{fullcc}</code>
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - {gateway}
⚡ 𝐑𝐞𝐬𝗽𝗼𝗻𝘀𝗲 - {response_message}

🔑 𝗜𝗻𝗳𝗼 - {brand} - {type} - {level}
🏦 𝐈𝐬𝐬𝐮𝐞𝐫 - {bank}
🌍 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} {flag}

⏳ 𝗧𝗶𝗺𝗲 - {time.perf_counter() - start:0.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀

👤 𝗥𝗲𝗾 𝗯𝘆: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ⤿ {role} ⤾
👑 𝗢𝘄𝗻𝗲𝗿: <a href="tg://user?id=7028548502">【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎</a>
"""
        await Client.edit_message_text(message.chat.id, checking_msg.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        print(f"Error: {str(e)}")
