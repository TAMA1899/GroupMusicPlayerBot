from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAACAgQAAx0CTv65QgABBfJlYF6VCrGMm6OJ23AxHmD6qUSWESsAAhoQAAKm8XEeD5nrjz5IJFYeBA")
    await message.reply_text(
        f"""<b>**Hello Friends**, {message.from_user.first_name}! 👋
\nSaya 𝐂𝐚𝐧𝐝𝐮𝐌𝐮𝐬𝐢𝐜𝐁𝐨𝐭, Saya akan membantumu **memutar music** di Voice Chat Telegram Groups & Channel, dengan **fitur-fitur** yang menarik.
\n─────────────────────────────────
𝑺𝒆𝒎𝒖𝒂 𝒐𝒓𝒂𝒏𝒈 𝒑𝒂𝒔𝒕𝒊 𝒎𝒂𝒕𝒊, 𝒕𝒂𝒑𝒊 𝒕𝒊𝒅𝒂𝒌 𝒔𝒆𝒎𝒖𝒂 𝒐𝒓𝒂𝒏𝒈 𝒅𝒂𝒑𝒂𝒕 𝒎𝒆𝒎𝒃𝒆𝒓𝒊 𝒂𝒓𝒕𝒊. 𝑷𝒂𝒔𝒕𝒊𝒌𝒂𝒏 𝒉𝒊𝒅𝒖𝒑𝒎𝒖 𝒃𝒆𝒓𝒂𝒓𝒕𝒊/𝒃𝒆𝒓𝒎𝒂𝒏𝒇𝒂𝒂𝒕 𝒖𝒏𝒕𝒖𝒌 𝒐𝒓𝒂𝒏𝒈 𝒍𝒂𝒊𝒏. 
─────────────────────────────────
\n❃ Manage by : [°ᴹᴿ° | ℝ𝕆𝔹𝕆𝕋](https://t.me/justthetech) 
❃ Support dengan doa aja guys! Thanks!
❃ NB : Maaf jika ada kekurangan didalam bot ini.
        </b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⁉️ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʀᴜʙ ⁉️", url=f"https://t.me/candumusic_bot?startgroup=true")
                ],
                [
                    InlineKeyboardButton(
                        "☕ ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/robotmusicupdate"), 
                    InlineKeyboardButton(
                        "ᴏᴡɴᴇʀ ☕", url=f"https://t.me/justthetech")
                ],
                [
                    InlineKeyboardButton(
                        "✍️ ᴅᴀꜰᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ✍️", url="https://telegra.ph/ROBOT-04-23-2"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**ROBOT MUSIC ONLINE** 📀""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☕ UPDATE ☕", url="https://t.me/robotmusicupdate")
                ]
            ]
        )
   )
        
@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""**Klick Tombol Untuk Daftar Perintah Bot**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✍️ ᴅᴀꜰᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ✍️", url="https://telegra.ph/ROBOT-04-23-2"
                    )
                ]
            ]
        ),
    )        
        
        


