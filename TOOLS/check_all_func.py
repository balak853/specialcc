from FUNC.usersdb_func import *
import time
from FUNC.defs import *

gate_active    = json.loads(open("FILES/deadsk.json", "r" , encoding="utf-8").read())["gate_active"]


async def check_all_thing(Client , message):
    try:
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        user_id   = str(message.from_user.id)
        chat_type = str(message.chat.type)
        chat_id   = str(message.chat.id)
        regdata   = await getuserinfo(user_id)
        regdata   = str(regdata)
        if regdata == "None":
            resp = f"""<b>
Unregistered Users ⚠️

Message: You Can't Use Me Unless You Register First .

Type /register to Continue
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False , False

        if any(command in message.text for command in gate_active):
            resp = "<b>The Gate Is Not Available For The Use Right Now Nigga ❌</b>"
            await message.reply_text(resp, reply_to_message_id=message.id)
            return False, False, False

        getuser        = await getuserinfo(user_id)
        status         = getuser["status"]
        credit         = int(getuser["credit"])
        antispam_time  = int(getuser["antispam_time"])
        now            = int(time.time())
        count_antispam = now - antispam_time
        checkgroup     = await getchatinfo(chat_id)
        checkgroup     = str(checkgroup)
        await plan_expirychk(user_id)

        if chat_type == "ChatType.PRIVATE" and status == "FREE":
            resp = f"""<b>
Premium Users Required ⚠️

Message: Only Premium Users are Allowed to use bot in Personal . Although You Can Use Bot Free Here https://t.me/+2ky3NvWYvaM4ZGNl

Buy Premium Plan Using /buy 
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id, disable_web_page_preview=True)
            return False , False

        if (
            chat_type == "ChatType.GROUP"
            or chat_type == "ChatType.SUPERGROUP"
            and checkgroup == "None"
        ):
            resp = f"""<b>
Unauthorized Chats ⚠️

Message: Only Chats Approved By @BALAK_TRUSTED Can Only Use Me . To Get Approve Your Chat Follow The Steps .

Type /howgp to Know The Steps
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        if credit < 5:
            resp = f"""<b>
Insufficient Credits ⚠️

Message: You Have Insufficient Credits to Use Me . Recharge Credit For Using Me

Type /buy to Recharge
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        if status == "ELITE" and count_antispam < 5:
            after = 5 - count_antispam
            resp = f"""<b>
Antispam Detected ⚠️

Message: Nigga You Are Spamming Very  Fast . Try After {after}s to Use Me Again .

Reduce Antispam Time /buy Using Paid Plan
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        if status == "FREE" and count_antispam < 20:
            after = 20 - count_antispam
            resp = f"""<b>
Antispam Detected ⚠️

Message: Nigga You Are Spamming Very Fast . Try After {after}s to Use Me Again .

Reduce Antispam Time /buy Using Paid Plan
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        return True , status
    

    except:
        import traceback
        await error_log(traceback.format_exc())
        try:
            await message.reply_text("Try Again later" ,  reply_to_message_id = message.id)
        except:
            pass
        return False , False 


async def check_some_thing(Client , message):
    try:
        user_id   = str(message.from_user.id)
        chat_type = str(message.chat.type)
        chat_id   = str(message.chat.id)
        regdata   = await getuserinfo(user_id)
        regdata   = str(regdata)
        if regdata == "None":
            resp = f"""<b>
Unregistered Users ⚠️

Message: You Can't Use Me Unless You Register First .

Type /register to Continue
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        getuser    = await getuserinfo(user_id)
        status     = getuser["status"]
        checkgroup = await getchatinfo(chat_id)
        checkgroup = str(checkgroup)
        await plan_expirychk(user_id)

        if chat_type == "ChatType.PRIVATE" and status == "FREE":
            resp = """<b>
Premium Users Required ⚠️

Message: Only Premium Users are Allowed to use bot in Personal . Although You Can Use Bot Free Here https://t.me/+tYnbEVtZ4cw3MzA9

Buy Premium Plan Using /buy
</b>"""
            await message.reply_text(resp , message_id=message.id, disable_web_page_preview=True)
            return False , False

        if (
            chat_type == "ChatType.GROUP"
            or chat_type == "ChatType.SUPERGROUP"
            and checkgroup == "None"
        ):
            resp = f"""<b>
Unauthorized Chats ⚠️

Message: Only Chats Approved By @BALAK_TRUSTED Can Only Use Me . To Get Approve Your Chat Follow The Steps .

Type /howgp to Know The Steps
</b>"""
            await message.reply_text(resp ,  reply_to_message_id = message.id)
            return False , False

        return True , status

    except:
        import traceback
        await error_log(traceback.format_exc())
        try:
            await message.reply_text("Request Failed ❌" ,  reply_to_message_id = message.id)
        except:
            pass
        return False , False


