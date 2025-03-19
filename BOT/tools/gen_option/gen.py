import httpx
import os
import asyncio
import time
import threading
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from FUNC.cc_gen import *
from TOOLS.check_all_func import *

# ✅ Fast Luhn Algorithm (Direct Valid CC Generate)
def generate_luhn_valid(cc_prefix):
    import random
    cc_body = cc_prefix + "".join(random.choices("0123456789", k=15-len(cc_prefix)))
    total = sum(int(d) * 2 - 9 if (i % 2) else int(d) for i, d in enumerate(reversed(cc_body)))
    check_digit = (10 - (total % 10)) % 10
    return cc_body + str(check_digit)

# ✅ Generate a Single Card
def cc_generator(cc, mes, ano, cvv):
    import random
    if mes in ["None", "X", "x", "rnd"]:
        mes = f"{random.randint(1, 12):02d}"
    if ano in ["None", "X", "x", "rnd"]:
        ano = str(random.randint(2024, 2035))
    if cvv in ["None", "X", "x", "rnd"]:
        cvv = str(random.randint(100, 999)) if cc.startswith(("4", "5")) else str(random.randint(1000, 9999))

    return f"{generate_luhn_valid(cc)}|{mes}|{ano}|{cvv}"

# ✅ Multi-threaded Generator (Super Fast!)
async def luhn_card_generator(cc, mes, ano, cvv, amount):
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, cc_generator, cc, mes, ano, cvv) for _ in range(amount)]
    cards = await asyncio.gather(*tasks)
    return "\n".join(cards)

# ✅ Generate Code Blocks for Telegram
def generate_code_blocks(all_cards):
    return "\n".join(f"<code>{card}</code>" for card in all_cards.split("\n"))

# ✅ Telegram Command Handler
@Client.on_message(filters.command("gen", [".", "/"]))
def multi(client, message):
    threading.Thread(target=bcall, args=(client, message)).start()

def bcall(client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gen_cmd(client, message))
    loop.close()

# ✅ Main Command Logic
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
            mes = cc_parts[1] if len(cc_parts) > 1 else "None"
            ano = cc_parts[2] if len(cc_parts) > 2 else "None"
            cvv = cc_parts[3] if len(cc_parts) > 3 else "None"
        except IndexError:
            await message.reply_text(
                "<b>Wrong Format ❌</b>\n\n"
                "Usage:\n"
                "<code>/gen 447697</code> (Only Bin)\n"
                "<code>/gen 447697|12</code> (With Expiry)\n"
                "<code>/gen 447697|12|23</code>\n"
                "<code>/gen 447697|12|23|000</code> (With CVV)\n"
                "<code>/gen 447697 100</code> (Custom Amount)",
                message.id,
            )
            return

        amount = 10
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        if amount > 10000:
            await message.reply_text("<b>Limit Reached ⚠️ Maximum: 10K</b>", message.id)
            return

        delete = await message.reply_text("<b>Generating...</b>", message.id)
        start = time.perf_counter()

        session = httpx.AsyncClient(timeout=30)
        getbin = await get_bin_details(cc[:6])
        await session.aclose()

        brand, type_, level, bank, country, flag, currency = getbin

        all_cards = await luhn_card_generator(cc, mes, ano, cvv, amount)
        elapsed_time = time.perf_counter() - start

        if amount == 10:
            response = (
                f"- 𝐂𝐂 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 ✅\n"
                f"- 𝐁𝐢𝐧 - <code>{cc}</code>\n"
                f"- 𝐀𝐦𝐨𝐮𝐧𝐭 - {amount}\n\n"
                f"{generate_code_blocks(all_cards)}"
                f"- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}\n"
                f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
                f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag}\n\n"
                f"- 𝐓𝐢𝐦𝐞: {elapsed_time:.2f} sec\n"
                f"- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> [{role}]"
            )
            await client.delete_messages(message.chat.id, delete.id)
            await message.reply_text(response, message.id)
        else:
            filename = f"downloads/{amount}x_CC_Generated_By_{user_id}.txt"
            with open(filename, "w") as f:
                f.write(all_cards)

            caption = (
                f"- 𝐁𝐢𝐧: <code>{cc}</code>\n"
                f"- 𝐀𝐦𝐨𝐮𝐧𝐭: {amount}\n\n"
                f"- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}\n"
                f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
                f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag} - {currency}\n\n"
                f"- 𝐓𝐢𝐦𝐞: {elapsed_time:.2f} sec\n"
                f"- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> [{role}]"
            )
            await client.delete_messages(message.chat.id, delete.id)
            await message.reply_document(filename, caption=caption, reply_to_message_id=message.id)
            os.remove(filename)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
