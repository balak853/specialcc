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
        first_name = message.from_user.first_name
        mention_user = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        gateway = "3DS Lookup"
        approve = "𝗣𝗮𝘀𝘀𝗲𝗱 ✅"

        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return

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

        processing_msg = f"""<b>╔═══════════════════╗
     ↯ 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴...
╚═══════════════════╝

🃏 𝗖𝗖 - {fullcc}
🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  3DS Look Up 
⚡ 𝐑𝐞𝐬𝗽𝗼𝗻𝘀𝗲 - ■■■□ 70%

🔑 𝗥𝗲𝗾: {mention_user}</b>"""

        processing_reply = await message.reply_text(processing_msg, message.id, disable_web_page_preview=True)

        # Check vbvbin.txt file
        with open("FILES/vbvbin.txt", "r", encoding="utf-8") as file:
            vbv_data = file.readlines()

        bin_found = False
        bin_response, response_message = "Not Found", "Lookup Card Error"

        for line in vbv_data:
            if line.startswith(bin):
                bin_found = True
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    bin_response, response_message = parts[1], parts[2]
                if "3D TRUE ❌" in bin_response:
                    approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
                break

        if not bin_found:
            approve = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"

        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=100) as session:
            getbin = await get_bin_details(cc)

        brand, type, level, bank, country, flag = getbin

        finalresp = f"""<b>
{approve}
        
𝗖𝗮𝗿𝗱 ⇾ <code>{fullcc}</code>
𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ⇾ {gateway}
𝐑𝐞𝐬𝗽𝗼𝗻𝘀𝗲 ⇾ {response_message}

𝗜𝗻𝗳𝗼 ⇾ {brand} - {type} - {level}
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
𝐂𝐨𝐮𝗻𝘁𝗿𝐲 ⇾ {country} {flag}

𝗧𝗶𝗺𝗲 ⇾ {time.perf_counter() - start:.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀</b>"""

        await processing_reply.edit(finalresp, disable_web_page_preview=True)
        await setantispamtime(user_id)
        await deductcredit(user_id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        print(f"Error: {str(e)}")
