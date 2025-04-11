import httpx
import os
import threading
import asyncio
import time
import random
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *
from concurrent.futures import ThreadPoolExecutor


def generate_code_blocks(all_cards):
    code_blocks = ""
    cards = all_cards.split('\n')
    for card in cards:
        code_blocks += f"<code>{card}</code>\n"
    return code_blocks


@Client.on_message(filters.command("gen", [".", "/"]))
def multi(client, message):
    t1 = threading.Thread(target=bcall, args=(client, message))
    t1.start()


def bcall(client, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gen_cmd(client, message))
    loop.close()


def check_luhn(card_no):
    n_sum = 0
    is_second = False
    for i in range(len(card_no) - 1, -1, -1):
        d = int(card_no[i])
        if is_second:
            d *= 2
        n_sum += d // 10
        n_sum += d % 10
        is_second = not is_second
    return n_sum % 10 == 0


def cc_generator(cc, mes, ano, cvv):
    if mes and len(mes) == 1:
        mes = "0" + mes

    if ano and len(ano) == 2:
        ano = "20" + ano

    if cc[:2] in ["34", "37"]:
        length = 15
    else:
        length = 16

    cc_base = cc + ''.join(random.choices("0123456789", k=length))
    cc_gen = cc_base[:length]

    cc_gen = ''.join(
        str(random.randint(0, 9)) if x == 'x' else x
        for x in cc_gen
    )

    mes = mes if mes and "x" not in mes.lower() else f"{random.randint(1, 12):02d}"
    ano = ano if ano and "x" not in str(ano).lower() else str(random.randint(2024, 2035))

    if not cvv or 'x' in str(cvv).lower():
        if cc_gen.startswith(("34", "37")):
            cvv = str(random.randint(1000, 9999))
        else:
            cvv = str(random.randint(100, 999))

    return f"{cc_gen}|{mes}|{ano}|{cvv}"


def luhn_card_generator(cc, mes, ano, cvv, amount):
    cards = []
    while len(cards) < amount:
        result = cc_generator(cc, mes, ano, cvv)
        ccx, mesx, anox, cvvx = result.split("|")
        if check_luhn(ccx):
            cards.append(f"{ccx}|{mesx}|{anox}|{cvvx}")
    return "\n".join(cards)


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
            resp = """
Wrong Format ❌

Usage:
Only Bin
<code>/gen 447697</code>

With Expiration
<code>/gen 447697|12</code>
<code>/gen 447697|12|23</code>

With CVV
<code>/gen 447697|12|23|000</code>

With Custom Amount
<code>/gen 447697 100</code>
"""
            await message.reply_text(resp, message.id)
            return

        amount = 10
        try:
            amount = int(message.text.split()[2])
        except (IndexError, ValueError):
            pass

        if amount > 10000:
            await message.reply_text("<b>Limit Reached ⚠️\n\nMaximum Generated Amount is 10K.</b>", message.id)
            return

        delete = await message.reply_text("<b>Generating...</b>", message.id)
        start = time.perf_counter()

        session = httpx.AsyncClient(timeout=30)
        getbin = await get_bin_details(cc[:6])
        await session.aclose()
        brand, type_, level, bank, country, flag, currency = getbin

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            all_cards = await loop.run_in_executor(pool, luhn_card_generator, cc, mes, ano, cvv, amount)

        if amount == 10:
            resp = (
                f"- 𝐂𝐂 𝐆𝐞𝐧𝐚𝐫𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲\n"
                f"- 𝐁𝐢𝐧 - <code>{cc}</code>\n"
                f"- 𝐀𝐦𝐨𝐮𝐧𝐭 - {amount}\n\n"
                f"{generate_code_blocks(all_cards)}"
                f"- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}\n"
                f"- 𝐁𝐚𝐧𝐤 - {bank} 🏛\n"
                f"- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag}\n\n"
                f"- 𝐓𝐢𝐦𝐞: - {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬\n"
                f"- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href='tg://user?id={message.from_user.id}'> {message.from_user.first_name}</a> [ {role} ]"
            )
            await client.delete_messages(message.chat.id, delete.id)
            await message.reply_text(resp, message.id)
        else:
            filename = f"downloads/{amount}x_CC_Generated_By_{user_id}.txt"
            with open(filename, "w") as f:
                f.write(f"{all_cards}\n")

            caption = f"""
- 𝐁𝐢𝐧: <code>{cc}</code> 
- 𝐀𝐦𝐨𝐮𝐧𝐭: {amount}

- 𝗜𝗻𝗳𝗼 - {brand} - {type_} - {level}
- 𝐁𝐚𝐧𝐤 - {bank} 🏛  
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {country} - {flag} - {currency}

- 𝐓𝐢𝐦𝐞 - {time.perf_counter() - start:0.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
- 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 - <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> ⤿ {role} ⤾
"""
            await client.delete_messages(message.chat.id, delete.id)
            await message.reply_document(document=filename, caption=caption, reply_to_message_id=message.id)
            os.remove(filename)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
