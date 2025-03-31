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
        approve = "PASSED"

        checkall = await check_all_thing(Client, message)
        if checkall[0] == False:
            return

        role = checkall[1]
        getcc = await getmessage(message)
        if getcc == False:
            resp = f"""
<b>VBV CHECKER</b>
━━━━━━━━━━━━━━━━
<b>Gate Name:</b> {gateway}
<b>CMD:</b> /vbv

<b>No CC Found in your input!</b>

<b>Usage:</b> /vbv cc|mes|ano|cvv
━━━━━━━━━━━━━━━━"""
            await message.reply_text(resp, message.id)
            return

        cc, mes, ano, cvv = getcc[0], getcc[1], getcc[2], getcc[3]
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        bin = cc[:6]

        if bin.startswith('3'):
            await message.reply_text("Unsupported card type.", message.id)
            return
        
        processing_msg = "Processing your request..."
        processing_reply = await message.reply_text(processing_msg, message.id)
        
        with open("FILES/vbvbin.txt", "r", encoding="utf-8") as file:
            vbv_data = file.readlines()

        bin_found = False
        for line in vbv_data:
            if line.startswith(bin):
                bin_found = True
                bin_response = line.strip().split('|')[1]
                response_message = line.strip().split('|')[2]
                if "3D TRUE" in bin_response:
                    approve = "REJECTED"
                break

        if not bin_found:
            approve = "REJECTED"
            bin_response = "Not Found"
            response_message = "Lookup Card Error"
        
        start = time.perf_counter()
        session = httpx.AsyncClient(timeout=100)
        getbin = await get_bin_details(cc)
        await session.aclose()

        brand, type, level, bank, country, flag = getbin

        finalresp = f"""
<b>VBV CHECK RESULT</b>
━━━━━━━━━━━━━━━━
<b>Status:</b> {approve}

<b>Card:</b> <code>{fullcc}</code>
<b>Gateway:</b> {gateway}
<b>Response:</b> {response_message}

<b>Info:</b> {brand} - {type} - {level}
<b>Issuer:</b> {bank}
<b>Country:</b> {country}

<b>Time:</b> {time.perf_counter() - start:0.2f} sec
━━━━━━━━━━━━━━━━"""
        await Client.edit_message_text(message.chat.id, processing_reply.id, finalresp)
        await setantispamtime(user_id)
        await deductcredit(user_id)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
        print(f"Error: {str(e)}")
