import json
from pyrogram import Client, filters
from FUNC.usersdb_func import *


@Client.on_message(filters.command("cs", [".", "/"]))
async def cmd_cs(Client, message):
    try:
        user_id     = str(message.from_user.id)
        OWNER_ID    = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["OWNER_ID"]
        if user_id not in OWNER_ID:
            resp = """<b>╰┈➤𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐭𝐡𝐞 𝐁𝐨𝐬𝐬 ❤️!</b>"""
            await message.reply_text(resp, message.id)
            return

        user_id , module , value = message.text.split(" ")
        await updateuserinfo(user_id, module, value)

        resp = f"""<b>
𝐂𝐮𝐬𝐭𝐨𝐦 𝐈𝐧𝐟𝐨 𝐂𝐡𝐚𝐧𝐠𝐞𝐝 ✅
━━━━━━━━━━━━━━
𝐔𝐬𝐞𝐫_𝐈𝐃 : {user_id}
𝐊𝐞𝐲_𝐍𝐚𝐦𝐞 : {module}
𝐊𝐞𝐲_𝐕𝐚𝐥𝐮𝐞 : {value}

𝐒𝐭𝐚𝐭𝐮𝐬 : 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥
</b> """
        await message.reply_text(resp, message.id)

    except:
        import traceback
        await error_log(traceback.format_exc())
