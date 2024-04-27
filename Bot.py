import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(
    level=logging.INFO, format="%(name)s - [%(levelname)s] - %(message)s"
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID", ""))
api_hash = os.environ.get("API_HASH", "")
bot_token = os.environ.get("TOKEN", "")
client = TelegramClient("client", api_id, api_hash).start(bot_token=bot_token)
spam_chats = []


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("↢ انا علي قيد الحياه 👋")
    await event.reply(
        "اهلا 👋 \n🏷 وظيفتي هي منشن إلى كل عضو في المجموعة في رسالة واحده لجذب اهتمام الأعضاء\n👇 استخدم الأزرار أدناه لاستخدام الروبوت",
        link_preview=False,
        buttons=(
            [
                Button.url(
                    "‹ اضفني الي مجموعتك ›",
                    "https://t.me/TagAllRbot?startgroup=true",
                ),
            ],
            [
                Button.url("‹ الدعم ›", "https://t.me/ll_YARRO_KI_DUNIYA_II"),
                Button.url("‹ السورس ›", "https://t.me/wx_pm"),
            ],
            [
                Button.url("𝖣𝖾𝗏", "https://t.me/ToPTeTo"),
            ],
        ),
    )


@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("ᴅᴇᴀʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴғ 🥺")
    helptext = "↢ تفضل هذة قائمه المساعده 🔎\n1- استخدم امر ‹ تاك للكل ›\n2- لتعطيل الامر ‹ الغاء المنشن ›\n3- لوضع منشن على المسؤلين ‹ الادمنيه ›\n↢ كما تشاهد كيفيه عمل منشن للاعضاء ، مثال \nتاك للكل صباح الخير"
    await event.reply(
        helptext,
        link_preview=False,
        buttons=(
            [
                Button.url("الدعم", "https://t.me/wx_pm"),
                Button.url("اضفني الي مجموعتك", "https://t.me/TagAllRbot?startgroup=true"),
            ]
        ),
    )


@client.on(events.NewMessage(pattern="^المطور$"))
async def help(event):
    chat_id = event.chat_id
    if not event.is_private:
        return await event.respond("عزيزي يعتذر استعمال الامر هنا ارسلي خاص")
    helptext = "↢ اهلا بك انا بوت TagAll اعمل علي اقصي سرعه \nهذا هو مطوري ‹ [Tᴇᴛᴏ](https://t.me/ToPTeTo) ›"
    await event.reply(
        helptext,
        link_preview=False,
        buttons=(
            [
                Button.url("الدعم", "https://t.me/wx_pm"),
                Button.url("اضفني الي مجموعتك", "https://t.me/TagAllRbot?startgroup=true"),
            ]
        ),
    )


@client.on(events.NewMessage(pattern="^تاك للكل ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond(
            "هذا الامر فقط بالمجموعات والقنوات 🔍"
        )

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("فقط مشرفيني فقط الذي لديهم صلاحيات التحكم بي")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("__Give me one argument!__")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "__I can't mention members for older messages! (messages which are sent before I'm added to group)__"
            )
    else:
        return await event.respond(
            "قم بعمل ريبلي علي الرساله او قم باستعمال الامر هكذا تاك للكل صباح الخير 👋"
        )

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n{msg}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@client.on(events.NewMessage(pattern="^/admins|/admin|@admin|@admins ?(.*)"))
async def _(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ ᴍᴇɴᴛɪᴏɴ ᴀᴅᴍɪɴ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴍᴇɴᴛɪᴏɴ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "__ɪ ᴄᴀɴ'ᴛ ᴍᴇɴᴛɪᴏɴ ᴍᴇᴍʙᴇʀs ꜰᴏʀ ᴏʟᴅᴇʀ ᴍᴇssᴀɢᴇs! (ᴍᴇssᴀɢᴇs ᴡʜɪᴄʜ ᴀʀᴇ sᴇɴᴛ ʙᴇꜰᴏʀᴇ ɪ'ᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ)__"
            )
    else:
        return await event.respond(
            "__ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴏᴛʜᴇʀs!__"
        )

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    chat = await event.get_input_chat()
    async for x in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f" \n [{x.first_name}](tg://user?id={x.id})"
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n{msg}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@client.on(events.NewMessage(pattern="^الغاء المنشن$"))
async def cancel_spam(event):
    if not event.chat_id in spam_chats:
        return await event.respond("__There is no proccess on going...__")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.respond("تم إيقاف المنشن بنجاح √")


print("Don't forget to visit Source Tito. All rights reserved @wx_pm")
client.run_until_disconnected()
