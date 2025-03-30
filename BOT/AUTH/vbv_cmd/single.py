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
            resp = f"""<b>
Gate Name: {gateway} ♻️
CMD: /vbv

Message: No CC Found in your input ❌

Usage: /vbv cc|mes|ano|cvv</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        bin = cc[:6]

        if bin.startswith('3'):
            await message.reply_text("<b>Unsupported card type.</b>", message.id)
            return
        
        processing_reply = await message.reply_text("""
╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴...
╚═══════════════════╝

🃏 𝗖𝗖 - Processing...
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  3DS Look Up
⚡ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ■□□□ 30%
""", message.id)
        await asyncio.sleep(1)
        await Client.edit_message_text(message.chat.id, processing_reply.id, processing_reply.text.replace("30%", "70%"))
        await asyncio.sleep(1)
        await Client.edit_message_text(message.chat.id, processing_reply.id, processing_reply.text.replace("70%", "99%"))

        with open("FILES/vbvbin.txt", "r", encoding="utf-8") as file:
            vbv_data = file.readlines()

        bin_found = False
        for line in vbv_data:
            if line.startswith(bin):
                bin_found = True
                bin_response = line.strip().split('|')[1]
                response_message = line.strip().split('|')[2]
                if "3D TRUE ❌" in bin_response:
                    approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
                break

        if not bin_found:
            approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            bin_response = "Not Found"
            response_message = "Lookup Card Error"
        
        start = time.perf_counter()
        session = httpx.AsyncClient(timeout=100)
        getbin = await get_bin_details(cc)
        await session.aclose()

        brand, type, level, bank, country, flag = getbin if getbin else ("Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "")

        finalresp = f"""
{approve}
        
𝗖𝗮𝗿𝗱 ⇾ <code>{fullcc}</code>
𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ⇾ {gateway}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {response_message}

𝗜𝗻𝗳𝗼 ⇾ {brand} - {type} - {level}
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country} {flag}

𝗧𝗶𝗺𝗲 ⇾ {time.perf_counter() - start:0.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀

<b>𝗥𝗲𝗾 𝗯𝘆:-</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ⤿ {role} ⤾
<b>𝗢𝘄𝗻𝗲𝗿:-</b> <a href="tg://user?id=7028548502">【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎</a>

"""
        await Client.edit_message_text(message.chat.id, processing_reply.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        print(f"Error: {str(e)}")
