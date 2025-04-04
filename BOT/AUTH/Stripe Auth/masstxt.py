import json
import time
import traceback
import asyncio
import httpx
import aiofiles
from pyrogram import Client, filters
from datetime import timedelta
from FUNC.usersdb_func import *
from FUNC.defs import *
from .gate2 import *
from .response import *
from TOOLS.check_all_func import *
from TOOLS.getcc_for_mass import *


async def mchkfunc(fullcc, user_id):
    try:
        proxies = await get_proxy_format()
        session = httpx.AsyncClient(timeout=30, proxies=proxies)
        result = await create_cvv_charge(fullcc, session)
        getresp = await get_charge_resp(result, user_id, fullcc)
        response = getresp["response"]
        status = getresp["status"]
        await session.aclose()
        return f"Card↯ <code>{fullcc}</code>\n<b>Status - {status}</b>\n<b>Result -⤿ {response} ⤾</b>\n\n"
    except Exception as e:
        await error_log(str(e))
        return f"<code>{fullcc}</code>\n<b>Result - Declined ❌</b>\n"


@Client.on_message(filters.command("massautxt", [".", "/"]) & filters.reply)
async def mass_check(Client, message):
    try:
        user_id = str(message.from_user.id)
        first_name = str(message.from_user.first_name)

        # Check if the replied message contains a file
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.reply_text("❌ Please reply to a .txt file containing CCs!", reply_to_message_id=message.id)
            return

        # Ensure the file is a .txt
        file_info = message.reply_to_message.document
        if not file_info.file_name.endswith(".txt"):
            await message.reply_text("❌ Only .txt files are supported!", reply_to_message_id=message.id)
            return

        # Download and read the file asynchronously
        file_path = await message.reply_to_message.download()
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            content = await file.read()
            ccs = content.strip().split("\n")

        # Limit to 200 CCs
        if len(ccs) > 200:
            ccs = ccs[:200]
            await message.reply_text("⚠️ Only the first 200 CCs will be checked!", reply_to_message_id=message.id)

        resp = f"""
- 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 -  Stripe Auth
- 𝐂𝐂 𝐀𝐦𝐨𝐮𝐧𝐭 - {len(ccs)}
- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - Checking CCs for {first_name}
- 𝐒𝐭𝐚𝐭𝐮𝐬 - Processing...⌛️
        """
        nov = await message.reply_text(resp, reply_to_message_id=message.id)

        text = "<b>↯ Stripe Auth</b>\n"
        amt = 0
        start = time.perf_counter()

        # Load worker limit
        worker_num = int(json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["THREADS"])

        # Process CCs with asyncio
        tasks = [mchkfunc(i.strip(), user_id) for i in ccs]
        while tasks:
            batch = tasks[:worker_num]
            results = await asyncio.gather(*batch)
            for result in results:
                amt += 1
                text += result
                if amt % 5 == 0:
                    try:
                        await Client.edit_message_text(message.chat.id, nov.id, text)
                    except:
                        pass
            await asyncio.sleep(1)
            tasks = tasks[worker_num:]

        # Final results
        taken = str(timedelta(seconds=time.perf_counter() - start))
        hours, minutes, seconds = map(float, taken.split(":"))
        text += f"\n- 𝗧𝗶𝗺𝗲 -  {int(hours)}h {int(minutes)}m {int(seconds)}s"

        await Client.edit_message_text(message.chat.id, nov.id, text)
        await massdeductcredit(user_id, len(ccs))
        await setantispamtime(user_id)

    except Exception as e:
        await error_log(traceback.format_exc())
        await message.reply_text("❌ An error occurred while processing the file.", reply_to_message_id=message.id)
