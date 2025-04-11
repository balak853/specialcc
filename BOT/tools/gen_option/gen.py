import httpx
import os
import asyncio
import time
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.cc_gen import *
from TOOLS.check_all_func import *


def generate_code_blocks(all_cards):
    return "\n".join(f"<code>{card}</code>" for card in all_cards.split('\n') if card)


@Client.on_message(filters.command("gen", [".", "/"]))
async def gen_cmd(client, message):
    try:
        user_id = str(message.from_user.id)
        checkall = await check_all_thing(client, message)
        if not checkall[0]:
            return

        role = checkall[1]
        try:
            ccsdata = message.text.split()[1]
            cc_parts = ccsdata.split("|")
            cc = cc_parts[0]
            mes = cc_parts[1] if len(cc_parts) > 1 else None
            ano = cc_parts[2] if len(cc_parts) > 2 else None
            cvv = cc_parts[3] if len(cc_parts) > 3 else None
        except IndexError:
            await message.reply_text(
                """<b>Wrong Format ❌

Usage:
Only Bin
<code>/gen 447697</code>

With Expiration
<code>/gen 447697|12</code>
<code>/gen 447697|12|23</code>

With CVV
<code>/gen 447697|12|23|000</code>

With Custom Amount
<code>/gen 447697 100</code></b>""",
                reply_to_message_id=message.id
            )
            return

        amount = 10  # Default
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        if amount > 10000:
            await message.reply_text("<b>Limit Reached ⚠️\nMaximum Generated Amount is 10K.</b>", message.id)
            return

        notice = await message.reply_text("<b>Generating...</b>", reply_to_message_id=message.id)
        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=30) as session:
            brand, type_, level, bank, country, flag, currency = await get_bin_details(cc[:6])

        all_cards = await luhn_card_genarator(cc, mes, ano, cvv, amount)

        if amount == 10:
            resp = (
                f"- 𝐂𝐂 𝐆𝐞𝐧𝐚𝐫𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲\n"
                f"- 𝐁𝐢𝐧 - <code>{cc}</code>\n"
                f"- 𝐀𝐦𝐨𝐮𝐧𝐭 - {amount}\n\n"
                f"{generate_code_blocks(all_cards)}\n"
                f"- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}\n"
                f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
                f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag}\n\n"
                f"- 𝐓𝐢𝐦𝐞: - {time.perf_counter() - start:.2f}s\n"
                f"- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> [ {role} ]"
            )
            await client.delete_messages(message.chat.id, notice.id)
            await message.reply_text(resp, message.id)

        else:
            filename = f"downloads/{amount}x_CC_Generated_By_{user_id}.txt"
            with open(filename, "w") as f:
                f.write(all_cards)

            caption = f"""
- 𝐁𝐢𝐧: <code>{cc}</code> 
- 𝐀𝐦𝐨𝐮𝐧𝐭: {amount}

- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}
- 𝐁𝐚𝐧𝐤 - {bank} 🏛  
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag} - {currency}

- 𝐓𝐢𝐦𝐞 - {time.perf_counter() - start:.2f}s
- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ⤿ {role} ⤾
"""
            await client.delete_messages(message.chat.id, notice.id)
            await message.reply_document(
                document=filename,
                caption=caption,
                reply_to_message_id=message.id
            )
            os.remove(filename)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
