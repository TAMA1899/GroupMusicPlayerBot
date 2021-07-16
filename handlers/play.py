from os import path
from typing import Dict
from pyrogram import Client
from pyrogram.types import Message, Voice
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from callsmusic import callsmusic, queues
from helpers.admins import get_administrators
from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
from pyrogram import filters, emoji
from pyrogram.types import InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
import traceback
import os
import sys
from callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.admins import admins as a
import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import que
import json
import wget
chat_id = None

import logging
import asyncio
import string
import random
from telethon.utils import get_display_name
import re
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

appid = apihash = bottoken = None
# start the bot
print("Starting...")
try:
    apiid = config("API_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    xchannel = config("CHANNEL")
    welcome_msg = config("WELCOME_MSG")
    welcome_not_joined = config("WELCOME_NOT_JOINED")
    on_join = config("ON_JOIN", cast=bool)
    on_new_msg = config("ON_NEW_MSG", cast=bool)
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

if (apiid != None and apihash!= None and bottoken != None):
    try:
        BotzHub = TelegramClient('BotzHub', apiid, apihash).start(bot_token=bottoken)
    except Exception as e:
        print(f"ERROR!\n{str(e)}")
        print("Bot is quiting...")
        exit()
else:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

channel = xchannel.replace("@", "")

# join check
async def get_user_join(id):
    ok = True
    try:
        await BotzHub(GetParticipantRequest(channel=channel, participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok


@BotzHub.on(events.ChatAction())
async def _(event):
    if on_join is False:
        return
    if event.user_joined or event.user_added:
        user = await event.get_user()
        chat = await event.get_chat()
        title = chat.title if chat.title else "this chat"
        pp = await BotzHub.get_participants(chat)
        count = len(pp)
        mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
        name = user.first_name
        last = user.last_name
        if last:
            fullname = f"{name} {last}"
        else:
            fullname = name
        uu = user.username
        if uu:
            username = f"@{uu}"
        else:
            username = mention
        x = await get_user_join(user.id)
        if x is True:
            msg = welcome_msg.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
        else:
            msg = welcome_not_joined.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}"), Button.inline("UnMute Me", data=f"unmute_{user.id}")]
            await BotzHub.edit_permissions(event.chat.id, user.id, until_date=None, send_messages=False)
        
        await event.reply(msg, buttons=butt)


@BotzHub.on(events.NewMessage(incoming=True))
async def mute_on_msg(event):
    if event.is_private:
        return
    if on_new_msg is False:
        return
    x = await get_user_join(event.sender_id)
    temp = await BotzHub(GetFullUserRequest(event.sender_id))
    if x is False:
        if temp.user.bot:
            return
        nm = temp.user.first_name
        try:
            await BotzHub.edit_permissions(event.chat.id, event.sender_id, until_date=None, send_messages=False)
        except Exception as e:
            print(str(e))
            return
        await event.reply(f"Hey {nm}, seems like you haven't joined our channel. Please join @{channel} and then press the button below to unmute yourself!", buttons=[[Button.url("Channel", url=f"https://t.me/{channel}")], [Button.inline("UnMute Me", data=f"unmute_{event.sender_id}")]])


@BotzHub.on(events.callbackquery.CallbackQuery(data=re.compile(b"unmute_(.*)")))
async def _(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if uid == event.sender_id:
        x = await get_user_join(uid)
        nm = (await BotzHub(GetFullUserRequest(uid))).user.first_name
        if x is False:
            await event.answer(f"You haven't joined @{channel} yet!", cache_time=0, alert=True)
        elif x is True:
            try:
                await BotzHub.edit_permissions(event.chat.id, uid, until_date=None, send_messages=True)
            except Exception as e:
                print(str(e))
                return
            msg = f"Welcome to {(await event.get_chat()).title}, {nm}!\nGood to see you here!"
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
            await event.edit(msg, buttons=butt)
    else:
        await event.answer("You are an old member and can speak freely! This isn't for you!", cache_time=0, alert=True)

@BotzHub.on(events.NewMessage(pattern="/start"))
async def strt(event):
    await event.reply(f"Hi. I'm a force subscribe bot made specially for @{channel}!\n\nCheckout @BotzHub :)", buttons=[Button.url("Channel", url=f"https://t.me/{channel}"), Button.url("Repository", url="https://github.com/xditya/ForceSub")])

    
print("ForceSub Bot has started.\nDo visit @BotzHub!")
BotzHub.run_until_disconnected()


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer('Kamu Tidak Diizinkan!', show_alert=True)
            return
    return decorator


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Judul   : {title}", (51, 215, 255), font=font)
    draw.text((190, 590), f"Durasi  : {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views   : {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Request dari : {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")

@Client.on_message(
    filters.command("playlist")
    & filters.group
    & ~ filters.edited
)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text('Tidak Ada Playlist')
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style='md')
    msg = "**Lagu Yang Sedang Diputar** di {}".format(message.chat.title)
    msg += "\n\nJudul : "+ now_playing
    msg += "\nRequest Dari : "+by
    temp.pop(0)
    if temp:
        msg += '\n───────────────────────────'
        msg += '\n**Antrian Lagu :**'
        for song in temp:
            name = song[0]
            usr = song[1].mention(style='md')
            msg += f'\n\nJudul : {name}'
            msg += f'\nRequest Dari : {usr}\n'
    await message.reply_text(msg)    
    

# ============================= Settings =========================================

def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
    #if chat.id in active_chats:
        stats = 'Settings of **{}**'.format(chat.title)
        if len(que) > 0:
            stats += '\n\n'
            stats += 'Volume         : {}%\n'.format(vol)
            stats += 'Music Antrian  : `{}`\n'.format(len(que))
            stats += 'Music sekarang : **{}**\n'.format(queue[0][0])
            stats += 'Request by : {}'.format(queue[0][1].mention)
    else:
        stats = None
    return stats

@Client.on_message(
    filters.command("current")
    & filters.group
    & ~ filters.edited
)
async def ee(client, message):
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)              
    else:
        await message.reply('Tidak Ada Music')
               
    
@Client.on_callback_query(filters.regex(pattern=r'^(playlist)$'))
async def p_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat
    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'playlist':           
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Player is idle')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "**Lagu Yang Sedang Dimainkan** di {}".format(cb.message.chat.title)
        msg += "\n\nJudul : "+ now_playing
        msg += "\nRequest Dari : "+by
        temp.pop(0)
        if temp:
             msg += '\n───────────────────────────'
             msg += '\n**Antrian Lagu :**'
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n\nJudul : {name}'
                 msg += f'\nRequest Dari : {usr}\n'
        await cb.message.edit(msg)  
        
@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    global que
    global useer   
    lel = await message.reply("🔄 **Tunggu**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "GeezProject"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>Ingatlah untuk menambahkan {user.first_name} ke Channel Anda</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>⚠️ Jadikan Bot sebagai Admin dulu!</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        f"<b>{user.first_name} berhasil bergabung dengan Group anda</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} tidak dapat bergabung dengan grup Anda karena banyaknya permintaan bergabung! Pastikan pengguna tidak dibanned dalam grup."
                        f"\n\nAtau tambahkan @{ASSISTANT_NAME} secara manual ke Grup Anda dan coba lagi</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>{user.first_name} terkena banned dari Grup ini, Minta admin untuk mengirim perintah `/play` untuk pertama kalinya atau tambahkan @robotassisten secara manual</i>"
        )
        return
    text_links=None
    await lel.edit("🔎 **Mencari Lagu**")
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ **Lagu dengan durasi lebih dari** `{DURATION_LIMIT}` **menit. Tidak Diizinkan!**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("☕ ᴜᴘᴅᴀᴛᴇ", url="https://t.me/robotmusicupdate"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ ☕", url="https://t.me/justthetech"),
                ],
                [InlineKeyboardButton(text="❌", callback_data="cls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/031fc9e0713224a151a2e.png" 
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 **Music Sedang Diproses**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:25]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "❁ <b>Music</b> tidak ditemukan.\n❁ Ketik /play (judul lagu).\n❁ Ketik /search (judul lagu)."
            )
            print(str(e))
            return
        dlurl=url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("☕ ᴜᴘᴅᴀᴛᴇ", url="https://t.me/robotmusicupdate"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ ☕", url="https://t.me/justthetech"),
                ],
                [InlineKeyboardButton(text="❌", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Music Sedang Diproses**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        
        try:
          results = YoutubeSearch(query, max_results=6).to_dict()
        except:
          await lel.edit("**Beri Judul Lagu untuk diputar**")
        # Looks like hell. Aren't it?? FUCK OFF
        try:
            toxxt = "**Silahkan Pilih lagu yang ingin Anda Putar:**\n\n"
            j = 0
            useer=user_name
            emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]

            while j < 6:
                toxxt += f"{emojilist[j]} [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})\n"
                toxxt += f" ├ **Durasi** : {results[j]['duration']}\n"
                toxxt += f" ├ **Views** : {results[j]['views']}\n"
                toxxt += f" └ **Channel** : {results[j]['channel']}\n\n"

                j += 1            
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1️⃣", callback_data=f'plll 0|{query}|{user_id}'),
                        InlineKeyboardButton("2️⃣", callback_data=f'plll 1|{query}|{user_id}'),
                        InlineKeyboardButton("3️⃣", callback_data=f'plll 2|{query}|{user_id}'),
                    ],
                    [
                        InlineKeyboardButton("4️⃣", callback_data=f'plll 3|{query}|{user_id}'),
                        InlineKeyboardButton("5️⃣", callback_data=f'plll 4|{query}|{user_id}'),
                        InlineKeyboardButton("6️⃣", callback_data=f'plll 5|{query}|{user_id}'),
                    ],
                    [InlineKeyboardButton(text="❌", callback_data="cls")],
                ]
            )       
            await lel.edit(toxxt,reply_markup=koyboard,disable_web_page_preview=True)
            # WHY PEOPLE ALWAYS LOVE PORN ?? (A point to think)
            return
            # Returning to pornhub
        except:
            await lel.edit("**Tidak ada hasil yang cukup untuk dipilih.. Mulai bermain langsung..**")
                        
            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:25]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]

            except Exception as e:
                await lel.edit(
                "❁ <b>Music tidak ditemukan.</b> \n❁ Ketik /play (judul lagu).\n❁ Ketik /search (judul lagu)."
                )
                print(str(e))
                return
            dlurl=url
            dlurl=dlurl.replace("youtube","youtubepp")
            keyboard = InlineKeyboardMarkup(
            [
                    [
                    InlineKeyboardButton("☕ ᴜᴘᴅᴀᴛᴇ", url="https://t.me/robotmusicupdate"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ ☕", url="https://t.me/justthetech"),
                ],
                    [InlineKeyboardButton(text="❌", callback_data="cls")],
            ]
        )
            requested_by = message.from_user.first_name
            await generate_cover(requested_by, title, views, duration, thumbnail)
            file_path = await convert(youtube.download(url))   
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption = f"📋 **Judul :** [{title}]({url}) \n#️⃣ **Antrian** : {position}",
                   reply_markup=keyboard)
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**Voice Chat Group tidak aktif, Saya tidak dapat bergabung**")
            return
        await message.reply_photo(
            photo="final.png",
            caption = f"📋 **Judul :** [{title[:60]}]({url})\n⏱️ **Durasi :** {duration}\n" \
                    + f"👤 **Request Dari :** {message.from_user.mention}",
                   reply_markup=keyboard)

    os.remove("final.png")
    return await lel.delete()
    
@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que

    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_=cbd.split(None, 1)[1]
    #useer_id = cb.message.reply_to_message.from_user.id
    try:
        x,query,useer_id = typed_.split("|")      
    except:
        await cb.message.edit("Lagu Tidak ditemukan")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("❌ Bukan Kamu Yang Mencari Lagu!", show_alert=True)
        return
    await cb.message.edit("🎵 **Music Sedang Diproses**")
    x=int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name
    
    results = YoutubeSearch(query, max_results=6).to_dict()
    resultss=results[x]["url_suffix"]
    title=results[x]["title"][:25]
    thumbnail=results[x]["thumbnails"][0]
    duration=results[x]["duration"]
    views=results[x]["views"]
    url = f"https://youtube.com{resultss}"
    
    try:    
        duuration= round(duration / 60)
        if duuration > DURATION_LIMIT:
            await cb.message.edit(f"❌ Lagu lebih lama dari {DURATION_LIMIT} menit. Tidak Diizinkan!")
            return
    except:
        pass
    try:
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
            [
            [
                    InlineKeyboardButton("☕ ᴜᴘᴅᴀᴛᴇ", url="https://t.me/robotmusicupdate"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ ☕", url="https://t.me/justthetech"),
            ],
                    [InlineKeyboardButton("❌", callback_data="cls")],
            ]
        )
    requested_by = useer_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await converter.convert(youtube.download(url)) 
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(chat_id,
            photo="final.png",
            caption = f"📋 **Judul :** [{title[:60]}]({url})\n⏱️ **Durasi** : {duration}\n#️⃣ **Antrian** : {position}", 
                   reply_markup=keyboard,
        )
        os.remove("final.png")
        
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)

        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await b.send_photo(chat_id,
            photo="final.png",
            caption = f"📋 **Judul :** [{title[:60]}]({url})\n⏱ **Durasi :** {duration}\n" \
                    + f"👤 **Request Dari :** {r_by.mention}",
                    reply_markup=keyboard,
        )
        os.remove("final.png")    
