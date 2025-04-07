import json
from pyrogram import Client, filters
from FUNC.usersdb_func import updateuserinfo  # Make sure this exists

@Client.on_message(filters.command("cs", [".", "/"]))
async def cmd_cs(Client, message):
    try:
        sender_id = str(message.from_user.id)

        # Load OWNER_ID from config
        with open("FILES/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        OWNER_ID = config.get("OWNER_ID", [])
        if isinstance(OWNER_ID, str):
            OWNER_ID = [OWNER_ID]

        # Permission Check
        if sender_id not in OWNER_ID:
            resp = "<b>╰┈➤ 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐭𝐡𝐞 𝐁𝐨𝐬𝐬 ❤️!</b>"
            await message.reply_text(resp, reply_to_message_id=message.id)
            return

        # Parse command
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            usage = "<b>Usage:</b> /cs user_id key_name key_value"
            await message.reply_text(usage, reply_to_message_id=message.id)
            return

        _, user_id, module, value = parts

        # Update info
        await updateuserinfo(user_id, module, value)

        # Response
        resp = f"""<b>
𝐂𝐮𝐬𝐭𝐨𝐦 𝐈𝐧𝐟𝐨 𝐂𝐡𝐚𝐧𝐠𝐞𝐝 ✅
━━━━━━━━━━━━━━
𝐔𝐬𝐞𝐫_𝐈𝐃 : {user_id}
𝐊𝐞𝐲_𝐍𝐚𝐦𝐞 : {module}
𝐊𝐞𝐲_𝐕𝐚𝐥𝐮𝐞 : {value}

𝐒𝐭𝐚𝐭𝐮𝐬 : 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥
</b>"""
        await message.reply_text(resp, reply_to_message_id=message.id)

    except Exception:
        import traceback
        await message.reply_text(
            f"<b>Error:</b>\n<code>{traceback.format_exc()}</code>",
            reply_to_message_id=message.id
        )
