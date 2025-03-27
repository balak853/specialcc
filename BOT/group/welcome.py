from pyrogram import Client, filters
import random

welcome_gif = [
    "https://telegra.ph/file/a5a2bb456bf3eecdbbb99.mp4",
    "https://telegra.ph/file/03c6e49bea9ce6c908b87.mp4",
    "https://telegra.ph/file/9ebf412f09cd7d2ceaaef.mp4",
    "https://telegra.ph/file/293cc10710e57530404f8.mp4",
    "https://telegra.ph/file/506898de518534ff68ba0.mp4",
    "https://telegra.ph/file/dae0156e5f48573f016da.mp4",
    "https://telegra.ph/file/3e2871e714f435d173b9e.mp4",
    "https://telegra.ph/file/714982b9fedfa3b4d8d2b.mp4",
    "https://telegra.ph/file/876edfcec678b64eac480.mp4",
    "https://telegra.ph/file/6b1ab5aec5fa81cf40005.mp4",
    "https://telegra.ph/file/b4834b434888de522fa49.mp4",
]

MESSAGE = """<b>
👋 𝐇𝐞𝐲 {name}!
𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 ❤️

📜 𝐏𝐥𝐞𝐚𝐬𝐞 𝐟𝐨𝐥𝐥𝐨𝐰 𝐬𝐨𝐦𝐞 𝐫𝐮𝐥𝐞𝐬:
𝟏. 🚫 𝐃𝐨𝐧'𝐭 𝐬𝐞𝐧𝐝 𝐮𝐧𝐰𝐚𝐧𝐭𝐞𝐝 𝐥𝐢𝐧𝐤𝐬.
𝟐. 🚫 𝐃𝐨𝐧'𝐭 𝐬𝐩𝐚𝐦.
𝟑. 🚫 𝐏𝐫𝐨𝐦𝐨𝐭𝐢𝐨𝐧 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐢𝐬 𝐩𝐫𝐨𝐡𝐢𝐛𝐢𝐭𝐞𝐝.

✅ 𝐉𝐮𝐬𝐭 𝐩𝐫𝐞𝐬𝐬 /register 𝐨𝐧𝐜𝐞 𝐭𝐨 𝐜𝐨𝐧𝐭𝐢𝐧𝐮𝐞 𝐮𝐬𝐢𝐧𝐠 𝐦𝐞 🥰
</b>"""

@Client.on_message(filters.new_chat_members)
async def welcome(client, message):
    try:
        new_members = [u.mention for u in message.new_chat_members]
        names = ", ".join(new_members)
        text = MESSAGE.format(name=names)
        img = random.choice(welcome_gif)

        await message.reply_video(video=img, caption=text, quote=True)
    except Exception:
        pass
