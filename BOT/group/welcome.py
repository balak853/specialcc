from pyrogram import Client, filters
import os

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
        for user in message.new_chat_members:
            user_id = user.id
            name = user.mention

            # Get user's profile photos
            photos = await client.get_profile_photos(user_id)
            
            if photos:
                # Download latest profile photo
                photo_path = await client.download_media(photos[0].file_id)
            else:
                photo_path = None  # No profile picture available

            text = MESSAGE.format(name=name)

            if photo_path:
                await message.reply_photo(photo=photo_path, caption=text, quote=True)
                os.remove(photo_path)  # Delete the photo after sending
            else:
                await message.reply_text(text, quote=True)

    except Exception as e:
        print(f"Error in welcome message: {e}")
