import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from FUNC.defs import *
from FUNC.usersdb_func import *


HELP_SECTIONS = {

    "ADMIN": """<b>🔐 ADMIN COMMANDS
━━━━━━━━━━━━━━
👥 USER MANAGEMENT
/adduser     - Add New User
/deluser     - Delete User
/getuser     - Get User Info
/showuser    - Show All Users
/promote     - Promote User
/demote      - Demote User

📢 BROADCAST
/brod        - Broadcast Message
/msg         - Message To User

📊 BOT MANAGEMENT
/stats       - Bot Statistics
/serverstats - Server Stats
/restart     - Restart Bot
/geterror    - Get Error Logs
/gateoff     - Disable Gate
/gateon      - Enable Gate

🎁 GIFT CODE
/gc          - Generate Gift Code

💾 DATA
/import      - Import Data
/export      - Export Data

🔑 PROXY
/addproxy    - Add Proxy List

💳 PLANS
/plan0       - Set Free Plan
/plan1       - Set Plan 1
/plan2       - Set Plan 2
/plan3       - Set Plan 3
/setamt      - Set Amount</b>""",

    "AUTH": """<b>🔓 AUTH GATE COMMANDS
━━━━━━━━━━━━━━
🔷 BRAINTREE AUTH
/b3          - Braintree Auth [Single]
/mb3         - Braintree Auth [Mass]

🔷 STRIPE AUTH
/au          - Stripe Auth [Single]
/ac          - Stripe Auth Check

🔷 VBV / NON-VBV
/vbv         - VBV Check [Single]
/mvbv        - VBV Check [Mass]
/addvbv      - Add VBV BIN
/rmvbv       - Remove VBV BIN
/addvbvtoken - Add VBV Token

🔷 PK KEY
/pk          - PK Auth [Single]
/addpk       - Add PK Key
/addauthtoken - Add Auth Token</b>""",

    "CHARGE": """<b>💥 CHARGE GATE COMMANDS
━━━━━━━━━━━━━━
🔷 BRAINTREE CHARGE
/br          - Braintree Charge [Single]
/mbr         - Braintree Charge [Mass]

🔷 SHOPIFY GATES
/sh          - Shopify [ SH ]  [Single]
/msh         - Shopify [ SH ]  [Mass]
/sho         - Shopify [ SHO ] [Single]
/msho        - Shopify [ SHO ] [Mass]
/so          - Shopify [ SO ]  [Single]
/mso         - Shopify [ SO ]  [Mass]
/sg          - Shopify [ SG ]  [Single]
/msg         - Shopify [ SG ]  [Mass]
/setso       - Set Shopify SO Token

🔷 SITEBASED GATES
/chk         - Sitebased [ CHK ] [Single]
/mchk        - Sitebased [ CHK ] [Mass]
/st          - Sitebased [ ST ]  [Single]
/mst         - Sitebased [ ST ]  [Mass]

🔷 SK BASED GATES
/sk          - SK Based [Single]
/ss          - SK Based SS [Single]
/svv         - SK Dead SVV [Single]
/msvv        - SK Dead SVV [Mass]
/cvv         - SK CVV [Single]
/mcvv        - SK CVV [Mass]
/ccn         - SK CCN [Single]
/mccn        - SK CCN [Mass]
/fl          - FL Gate [Single]
/cs          - CS Gate [Single]
/fr          - FR Gate [Single]</b>""",

    "TOOLS": """<b>🛠 TOOLS COMMANDS
━━━━━━━━━━━━━━
💳 CARD TOOLS
/gen         - Card Generator
/bin         - BIN Lookup
/scrbin      - Scrape BIN from Site
/ccntxt      - CCN from TXT File
/cvvtxt      - CVV from TXT File
/svvtxt      - SVV from TXT File
/sktxt       - SK from TXT File

🔑 SK TOOLS
/scrsk       - Scrape SK from Site
/skinfo      - SK Info / Details
/skuser      - SK User Info
/skadd       - Add SK
/addsk       - Add SK to DB
/delsk       - Delete SK from DB
/rmsk        - Remove SK
/viewsk      - View All SKs
/setsk       - Set Your SK
/mysk        - View Your SK

🔍 LOOKUP TOOLS
/ip          - IP Lookup
/id          - Get Chat / User ID
/info        - Account Info
/host        - Host Info
/fake        - Generate Fake Info
/gpt         - GPT Query
/url         - URL Scrape

📊 STATS TOOLS
/gethits     - Get Hit Results
/ping        - Ping Bot
/scr         - Scraper</b>""",

    "USER": """<b>👤 USER COMMANDS
━━━━━━━━━━━━━━
🚀 GENERAL
/start       - Start Bot
/cmds        - All Commands Menu
/register    - Register Account
/redeem      - Redeem Gift Code
/credits     - Bot Credits
/buy         - Buy Premium Plan
/selfcmd     - Self Commands

📋 PLANS
/csplan      - CS Plan Info
/getplan1    - Get Plan 1 Info
/getplan2    - Get Plan 2 Info
/getplan3    - Get Plan 3 Info

🌐 PROXY
/setproxy    - Set Your Proxy
/rmproxy     - Remove Your Proxy
/viewproxy   - View Your Proxy

💳 PAYMENT INFO
/howcrd      - How to Pay via Card
/howgp       - How to Pay via GP
/howpm       - How to Pay via PM
/pm          - PM Info</b>"""
}


@Client.on_message(filters.command("help", [".", "/"]))
async def admin_help(client, message):
    try:
        user_id  = str(message.from_user.id)
        OWNER_ID = json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["OWNER_ID"]

        if user_id not in OWNER_ID:
            resp = "<b>You Don't Have Permission To Use This Command.\nContact Bot Owner @BALAK_TRUSTED !</b>"
            await message.reply_text(resp, message.id)
            return

        intro = """<b>🤖 BALAK BOT — ADMIN HELP PANEL
━━━━━━━━━━━━━━
Select a category below to view all commands.</b>"""

        buttons = [
            [
                InlineKeyboardButton("🔐 Admin",  callback_data="help_ADMIN"),
                InlineKeyboardButton("🔓 Auth",   callback_data="help_AUTH"),
            ],
            [
                InlineKeyboardButton("💥 Charge", callback_data="help_CHARGE"),
                InlineKeyboardButton("🛠 Tools",  callback_data="help_TOOLS"),
            ],
            [
                InlineKeyboardButton("👤 User",   callback_data="help_USER"),
            ],
            [
                InlineKeyboardButton("❌ Close",  callback_data="help_close"),
            ]
        ]

        await message.reply_text(
            intro,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception:
        import traceback
        await error_log(traceback.format_exc())


@Client.on_callback_query(filters.regex("^help_"))
async def help_callback(client, callback_query):
    try:
        data = callback_query.data.replace("help_", "")

        if data == "close":
            await callback_query.message.delete()
            return

        if data not in HELP_SECTIONS:
            await callback_query.answer("Section not found!", show_alert=True)
            return

        text = HELP_SECTIONS[data]

        back_button = [[InlineKeyboardButton("🔙 Back", callback_data="help_back")]]

        await callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        await callback_query.answer()

    except Exception:
        import traceback
        await error_log(traceback.format_exc())


@Client.on_callback_query(filters.regex("^help_back$"))
async def help_back_callback(client, callback_query):
    try:
        intro = """<b>🤖 BALAK BOT — ADMIN HELP PANEL
━━━━━━━━━━━━━━
Select a category below to view all commands.</b>"""

        buttons = [
            [
                InlineKeyboardButton("🔐 Admin",  callback_data="help_ADMIN"),
                InlineKeyboardButton("🔓 Auth",   callback_data="help_AUTH"),
            ],
            [
                InlineKeyboardButton("💥 Charge", callback_data="help_CHARGE"),
                InlineKeyboardButton("🛠 Tools",  callback_data="help_TOOLS"),
            ],
            [
                InlineKeyboardButton("👤 User",   callback_data="help_USER"),
            ],
            [
                InlineKeyboardButton("❌ Close",  callback_data="help_close"),
            ]
        ]

        await callback_query.message.edit_text(
            intro,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await callback_query.answer()

    except Exception:
        import traceback
        await error_log(traceback.format_exc())
