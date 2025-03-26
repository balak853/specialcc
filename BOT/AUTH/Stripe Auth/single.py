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

        gateway = "Stripe Auth"

        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""<b>
━━━━━━━━━━━━━━━
<b>NO CC FOUND</b>
━━━━━━━━━━━━━━━
<b>Gate Name:</b> {gateway}  
<b>Usage:</b> /au cc|mes|ano|cvv  
━━━━━━━━━━━━━━━
<b>Example:</b> <code>/au 4242424242424242|12|25|123</code>  
━━━━━━━━━━━━━━━</b>"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        firstresp = f"""<b>
━━━━━━━━━━━━━━━
<b>CHECKING...</b>
━━━━━━━━━━━━━━━
<b>Card:</b> <code>{fullcc}</code>  
<b>Gateway:</b> {gateway}  
<b>Response:</b> ■□□□  
━━━━━━━━━━━━━━━</b>"""
        await asyncio.sleep(0.5)
        firstchk = await message.reply_text(firstresp, message.id)

        secondresp = f"""<b>
━━━━━━━━━━━━━━━
<b>PROCESSING...</b>
━━━━━━━━━━━━━━━
<b>Card:</b> <code>{fullcc}</code>  
<b>Gateway:</b> {gateway}  
<b>Response:</b> ■■■□  
━━━━━━━━━━━━━━━</b>"""
        await asyncio.sleep(0.5)
        secondchk = await Client.edit_message_text(message.chat.id, firstchk.id, secondresp)

        start = time.perf_counter()
        proxies = await get_proxy_format()
        session = httpx.AsyncClient(timeout=30, follow_redirects=True)
        result = await create_cvv_charge(fullcc, session)
        getbin = await get_bin_details(cc)
        getresp = await get_charge_resp(result, user_id, fullcc)
        status = getresp["status"]
        response = getresp["response"]

        thirdresp = f"""<b>
━━━━━━━━━━━━━━━
<b>FINALIZING...</b>
━━━━━━━━━━━━━━━
<b>Card:</b> <code>{fullcc}</code>  
<b>Gateway:</b> {gateway}  
<b>Response:</b> ■■■■  
━━━━━━━━━━━━━━━</b>"""
        await asyncio.sleep(0.5)
        thirdcheck = await Client.edit_message_text(message.chat.id, secondchk.id, thirdresp)

        brand = getbin[0]
        type = getbin[1]
        level = getbin[2]
        bank = getbin[3]
        country = getbin[4]
        flag = getbin[5]
        currency = getbin[6]

        finalresp = f"""<b>
━━━━━━━━━━━━━━━
<b>TRANSACTION RESULT</b>
━━━━━━━━━━━━━━━
<b>Card:</b> <code>{fullcc}</code>  
<b>Gateway:</b> {gateway}  
<b>Status:</b> {status}  
<b>Response:</b> {response}  
━━━━━━━━━━━━━━━
<b>CARD INFO</b>  
━━━━━━━━━━━━━━━
<b>Brand:</b> {brand}  
<b>Type:</b> {type}  
<b>Level:</b> {level}  
<b>Bank:</b> {bank}  
<b>Country:</b> {country} {flag}  
<b>Currency:</b> {currency}  
━━━━━━━━━━━━━━━
<b>Time Taken:</b> {time.perf_counter() - start:0.2f} seconds  
━━━━━━━━━━━━━━━
<b>Checked by:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>  
<b>Developer:</b> <a href="tg://user?id=7297683223">Goku</a>  
━━━━━━━━━━━━━━━</b>"""
        await asyncio.sleep(0.5)
        await Client.edit_message_text(message.chat.id, thirdcheck.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)
        if status == "Approved":
            await sendcc(finalresp, session)
        await session.aclose()

    except:
        import traceback
        await error_log(traceback.format_exc())
