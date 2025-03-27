import traceback, json
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from datetime import date
from datetime import timedelta


@Client.on_message(filters.command("plan0", [".", "/"]))
async def cmd_plan0(Client, message):
    try:
        user_id     = str(message.from_user.id)
        OWNER_ID    = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["OWNER_ID"]
        if user_id not in OWNER_ID:
            resp = """<b>╰┈➤𝑨𝒃𝒆 𝑮𝒂𝒏𝒅𝒖 𝑻𝒖 𝑶𝒘𝒏𝒆𝒓 𝑯𝒂𝒊 𝑲𝒚𝒂 🧡!</b>"""
            await message.reply_text(resp, message.id)
            return

        user_id            = message.text.split(" ")[1]
        paymnt_method      = "OWNER"
        registration_check = await getuserinfo(user_id)
        registration_check = str(registration_check)
        if registration_check == "None":
            resp = f"""<b>
𝐎𝐰𝐧𝐞𝐫 𝐏𝐥𝐚𝐧 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐢𝐨𝐧 𝐅𝐚𝐢𝐥𝐞𝐝 ❌
━━━━━━━━━━━━━━
𝐔𝐬𝐞𝐫 𝐈𝐃 : <a href="tg://user?id={user_id}"> {user_id}</a> 
𝐏𝐥𝐚𝐧 𝐍𝐚𝐦𝐞 : 𝐎𝐰𝐧𝐞𝐫 𝐏𝐥𝐚𝐧 
𝐑𝐞𝐚𝐬𝐨𝐧 : 𝐔𝐧𝐫𝐞𝐠𝐢𝐬𝐭𝐞𝐫𝐞𝐝 𝐔𝐬𝐞𝐫𝐬

𝐒𝐭𝐚𝐭𝐮𝐬 : 𝐅𝐚𝐢𝐥𝐞𝐝
</b>"""
            await message.reply_text(resp, message.id)
            return

        await check_negetive_credits(user_id)
        await get_owner_plan(user_id)
        receipt_id  = await randgen(len=10)
        gettoday    = str(date.today()).split("-")
        yy          = gettoday[0]
        mm          = gettoday[1]
        dd          = gettoday[2]
        today       = f"{dd}-{mm}-{yy}"
        getvalidity = str(date.today() + timedelta(days=9999)).split("-")
        yy          = getvalidity[0]
        mm          = getvalidity[1]
        dd          = getvalidity[2]
        validity    = f"{dd}-{mm}-{yy}"

        user_resp = f"""<b>
𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐏𝐮𝐫𝐜𝐡𝐚𝐬𝐢𝐧𝐠 𝐎𝐰𝐧𝐞𝐫 𝐏𝐥𝐚𝐧 ✅

𝐈𝐃 : <code>{user_id}</code>
𝐏𝐥𝐚𝐧 : 𝐎𝐰𝐧𝐞𝐫
𝐏𝐫𝐢𝐜𝐞 : ∞ $
𝐏𝐮𝐫𝐜𝐡𝐚𝐬𝐞 𝐃𝐚𝐭𝐞 : {today}
𝐄𝐱𝐩𝐢𝐫𝐲 : {validity}
𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲: ∞ 𝐃𝐚𝐲𝐬
𝐒𝐭𝐚𝐭𝐮𝐬 : 𝐏𝐚𝐢𝐝 ☑️
𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐌𝐞𝐭𝐡𝐨𝐝 : {paymnt_method}.
𝐑𝐞𝐜𝐞𝐢𝐩𝐭 𝐈𝐃 : 𝐒𝐧𝐨✘-{receipt_id}

𝐓𝐡𝐢𝐬 𝐢𝐬 𝐚 𝐫𝐞𝐜𝐞𝐢𝐩𝐭 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐩𝐥𝐚𝐧.𝐒𝐚𝐯𝐞 𝐢𝐭 𝐬𝐞𝐜𝐮𝐫𝐞𝐥𝐲.𝐓𝐡𝐢𝐬 𝐰𝐢𝐥𝐥 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐢𝐟 𝐚𝐧𝐲𝐭𝐡𝐢𝐧𝐠 𝐠𝐨𝐞𝐬 𝐰𝐫𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐲𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞𝐬.

𝐇𝐚𝐯𝐞 𝐚 𝐆𝐨𝐨𝐝 𝐃𝐚𝐲!
</b>"""
        try:
            await Client.send_message(user_id, user_resp)
        except:
            pass

        ad_resp = f"""<b>
𝐆𝐨𝐥𝐝 𝐏𝐥𝐚𝐧 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 ✅ 
━━━━━━━━━━━━━━
𝐔𝐬𝐞𝐫 𝐈𝐃 : <a href="tg://user?id={user_id}"> {user_id}</a> 
𝐏𝐥𝐚𝐧 𝐍𝐚𝐦𝐞 : 𝐎𝐰𝐧𝐞𝐫 𝐏𝐥𝐚𝐧
𝐏𝐥𝐚𝐧 𝐄𝐱𝐩𝐢𝐫𝐲 : {validity} 

𝐒𝐭𝐚𝐭𝐮𝐬 : 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥!
        </b>"""
        await message.reply_text(ad_resp, message.id)

    except:
        import traceback
        await error_log(traceback.format_exc())
