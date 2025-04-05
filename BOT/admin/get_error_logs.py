import json
import os
from pyrogram import Client, filters
from FUNC.defs import *

@Client.on_message(filters.command("geterror", [".", "/"]))
async def cmd_geterror(Client, message):
    try:
        user_id = str(message.from_user.id)
        OWNER_ID = json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["OWNER_ID"]

        if user_id not in OWNER_ID:
            resp = (
                "<b>You Don't Have Permission To Use This Command.\n"
                "Contact Bot Owner @BALAK_TRUSTED !</b>"
            )
            await message.reply_text(resp, reply_to_message_id=message.id)
            return

        delete = await message.reply_text("<b>Getting Error Logs...</b>", reply_to_message_id=message.id)

        for log_file in ["error_logs.txt", "result_logs.txt"]:
            if os.path.exists(log_file):
                with open(log_file, "rb") as f:
                    await message.reply_document(document=f, reply_to_message_id=message.id)
                os.remove(log_file)
            else:
                await message.reply_text(f"<b>{log_file} file not found.</b>", reply_to_message_id=message.id)

        await Client.delete_messages(message.chat.id, delete.id)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
