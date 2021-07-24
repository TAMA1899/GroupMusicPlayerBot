from pyrogram import Client
from pyrogram.types import ChatMemberUpdated

from cache import admins as cache
from function import *

@Client.on_chat_member_updated()
async def chat_member_updated(_, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member \
            and chat_member_updated.old_chat_member:
        (
            admins.admins[chat_member_updated.chat.id].append(
                chat_member_updated.new_chat_member.user.id,
            )
        ) if (
            (
                chat_member_updated.new_chat_member.can_manage_voice_chats
            ) and (
                (
                    chat_member_updated.new_chat_member.user.id
                ) not in admins.admins[chat_member_updated.chat.id]
            )
        ) else (
            admins.admins[chat_member_updated.chat.id].remove(
                chat_member_updated.new_chat_member.user.id,
            )
        ) if (
            (
                chat_member_updated.new_chat_member.user.id
            ) in admins.admins[chat_member_updated.chat.id]
        ) else None

@Client.on_chat_member_updated()
async def chat_member_updated(_, chat_member_updated: ChatMemberUpdated):
    chat = chat_member_updated.chat.id
    new = chat_member_updated.new_chat_member

    if new.can_manage_voice_chats:
        if new.user.id not in cache.admins[chat]:
            cache.admins[chat].append(new.user.id)
    else:
        if new.user.id in cache.admins[chat]:
            cache.admins[chat].remove(new.user.id)
