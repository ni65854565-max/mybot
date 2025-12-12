import os
import re
import time
import json
import random
import asyncio
import logging
import sqlite3
from datetime import datetime
from traceback import format_exc
from telethon import TelegramClient, events, errors, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.types import InputPhoto, InputDocument
from config import ADMINS, API_ID, API_HASH, get_random_device

Date_Expire = 20270404


def add_data(data):
    try:

        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS file (
                ide INTEGER PRIMARY KEY,
                acsses_hash INT NOT NULL,
                file_ref BLOB NOT NULL,
                file_type TEXT NOT NULL
            );""")

        cursor.execute(
            f"INSERT INTO file (ide, acsses_hash,file_ref,file_type) VALUES (?, ?, ?,?)", data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


class Config:
    api_id = API_ID
    api_hash = API_HASH


class Login:
    def __init__(self, Config):
        logging.basicConfig(
            format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO)

    def return_client(self):
        try:
            os.mkdir("client")
        except Exception:
            pass
        app_version = "1.35.1 (1359)"
        list_dir = os.listdir("client")
        if len(list_dir) == 0:
            rand_dev = get_random_device()

            device_model = f"""{str(rand_dev["MANUFACTURER"]).lower()}{str(rand_dev["MODEL"])}"""

            system_version = f"SDK {rand_dev['SDK']}"
            client = TelegramClient(
                StringSession(),
                Config.api_id,
                Config.api_hash,
                app_version=app_version,
                device_model=device_model,
                system_version=system_version,
            )
            client._init_request = functions.InitConnectionRequest(
                api_id=Config.api_id,
                device_model=device_model,
                system_version=system_version,
                app_version=app_version,
                lang_code="en",
                system_lang_code="en",
                lang_pack='android',
                params=None,
                query=None
            )
            client.start()
            string_session = client.session.save()  # type: ignore

            string = {"api_id": Config.api_id,
                      "api_hash": Config.api_hash, "StringSession": string_session, "device_model": device_model,
                      "system_version": system_version,
                      "app_version": app_version, }

            open("client/client.json", "w").write(json.dumps(string))

            return client
        else:
            file = open("client/client.json", "r")
            user_id = json.load(file)
            session = user_id["StringSession"]
            device_model = user_id["device_model"]
            system_version = user_id["system_version"]
            client = TelegramClient(
                StringSession(session),
                Config.api_id,
                Config.api_hash,
                app_version=app_version,
                device_model=device_model,
                system_version=system_version,
            )
            client._init_request = functions.InitConnectionRequest(
                api_id=Config.api_id,
                device_model=device_model,
                system_version=system_version,
                app_version=app_version,
                lang_code="en",
                system_lang_code="en",
                lang_pack='android',
                params=None,
                query=None
            )
            client.start()
            return client

def check_telegram_link(link):
    patterns = {
        'invite_link': r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:joinchat/|\+))([\w-]+)$",
        'profile_link': r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/)([\w-]+)$",
        'username_link': r"^@([\w-]+)$",
    }

    for key, pattern in patterns.items():
        match = re.match(pattern, link)
        if match:
            return (key, match.groups())
class Main:
    def __init__(self):
        if "cloner.json" not in os.listdir():
            data = {"run": "0", "text": "@", "sleep": "2", "impolite": [], "chat": "", "answer": 10, "id": [], "tag": "off", "fosh": [], "admin": [], "enemys": [], "mute": [], "mode": "text", "id_msg": "", "from_id": "", "media": {
                "caption": "addmedia", "img": False, "file_id": 6007991306675032223, "access_hash": 9068375890150151571, "file_reference": "\\x01\\x00\\x00\\x04\\xae\\xad\\t\\xc7\\xd5\\xaf\\xf6\\x97\\x7\\x2\\x01\\xd0L{c\\x7f\\x\\x1dc\\x9c"}}
            open("cloner.json", "w").write(json.dumps(data))
        self.client = Login(Config).return_client()

    def get_server_load(self):
        return os.getloadavg()

    def bot(self):
        send_list = []

        async def send_file(sender_id, msg_id=None):
            conn = sqlite3.connect("db.db")
            v = conn.execute("SELECT * from file")
            v = random.choice(v.fetchall())
            if not msg_id:
                sender_id = await self.client.get_input_entity(sender_id)
            else:
                with open("cloner.json") as r:
                    af = json.load(r)
                sender_id = int(af["chat"])

            if v[3] == "img":
                doc = InputPhoto(id=int(v[0]),
                                 access_hash=int(v[1]),
                                 file_reference=v[2])
              
                if msg_id:
                    msg = await self.client.send_file(sender_id, doc, thumb="photo.jpg", reply_to=msg_id)
                    return
                msg = await self.client.send_file(sender_id, doc, thumb="photo.jpg")
                return
            else:
                doc = InputDocument(id=int(v[0]),
                                    access_hash=int(v[1]),
                                    file_reference=v[2])
                if msg_id:
                    msg = await self.client.send_file(sender_id, doc, reply_to=msg_id)
                    return
                msg = await self.client.send_file(sender_id, doc)
                return

        def converter(event):
            photo = False
            try:
                result = event.media.photo
                photo = True
            except:
                result = event.media.document
                photo = False
            return {"photo": photo, "result": result}

        @self.client.on(events.NewMessage(pattern="(?i)bot|ربات"))
        async def ping2(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("🌱 O N L I N E")

        @self.client.on(events.NewMessage(pattern="ممد"))
        async def ping(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("جون")

        @self.client.on(events.NewMessage(pattern="(?i)status|وضعیت"))
        async def show_stats(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                me = await self.client.get_me()
                if isinstance(me, types.User):
                    stats_message = (
                        f"✏️ Name : `{me.first_name}`\n"
                        f"👾 UserName : `{me.username}`\n"
                        f"👤 ID : `{me.id}`\n"
                        f"👥 Target : `{v['chat']}`\n"
                        f"⚡️ Speep time: `{v['sleep']}`\n"
                        f"👑 Admins : `{', '.join(map(str, v['admin']))}`\n"
                        f" ⚔Enemies : `{', '.join(map(str, v['enemys']))}`\n"
                        f"🔇 Muted : `{', '.join(map(str, v['mute']))}`\n"
                        f"🔧 Mode : `{v['mode']}`"
                    )
                    await event.reply(stats_message)
                else:
                    await event.reply("error in get the profile")

        @self.client.on(events.NewMessage(pattern="(?i)mute|سکوت"))
        async def silence_user2(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                args = event.message.message.split()
                user_to_silence_id = None
                if event.is_reply:
                    replied_msg = await event.get_reply_message()
                    user_to_silence_id = replied_msg.sender_id
                elif len(args) > 1 and args[1].isdigit():
                    user_to_silence_id = int(args[1])
                if user_to_silence_id not in v["mute"]:
                    v["mute"].append(user_to_silence_id)
                    with open("cloner.json", "w") as w:
                        json.dump(v, w)
                    await event.reply("**🔇user was added to the silence list.**")
                else:
                    await event.reply("**🔇user is already on the silent list.**")

        @self.client.on(events.NewMessage(pattern="(?i)unmute|حذف سکوت"))
        async def unsilence_user2(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                user_to_unsilence_id = None
                args = event.message.message.split()
                if event.is_reply:
                    replied_msg = await event.get_reply_message()
                    user_to_unsilence_id = replied_msg.sender_id
                elif len(args) > 1 and args[1].isdigit():
                    user_to_unsilence_id = int(args[1])
                if user_to_unsilence_id in v["mute"]:
                    v["mute"].remove(user_to_unsilence_id)
                    with open("cloner.json", "w") as w:
                        json.dump(v, w)
                    await event.reply("**🔉user was removed from the silence list.**")
                else:
                    await event.reply("**🔉user is not on the silent list.**")

        @self.client.on(events.NewMessage(pattern="(?i)unmuteall|پاکسازی لیست سکوت"))
        async def clear_silence_list2(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                v["mute"] = []
                with open("cloner.json", "w") as w:
                    json.dump(v, w)
                await event.reply("**🔊The silence list has been cleared successfully.**")

        @self.client.on(events.NewMessage(pattern="(?i)listmute|لیست سکوت"))
        async def view_silence_list2(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                silence_list = "\n".join(str(user_id) for user_id in v["mute"])
                if silence_list:
                    await event.reply(f"**💬the silence list**:\n `{silence_list}`")
                else:
                    await event.reply("**😕silence list is empty.**")

        @self.client.on(events.NewMessage(pattern="(?i)impolite|مبتذل"))
        async def silence_user(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                args = event.message.message.split()
                user_to_silence_id = None
                if event.is_reply:
                    replied_msg = await event.get_reply_message()
                    user_to_silence_id = replied_msg.sender_id
                elif len(args) > 1 and args[1].isdigit():
                    user_to_silence_id = int(args[1])
                if user_to_silence_id not in v["impolite"]:
                    v["impolite"].append(user_to_silence_id)
                    with open("cloner.json", "w") as w:
                        json.dump(v, w)
                    await event.reply("**🚽user was added to the vulgar list.**")
                else:
                    await event.reply("**🚽user is already on the vulgar list.**")

        @self.client.on(events.NewMessage(pattern="(?i)delimpolite|حذف مبتذل"))
        async def unsilence_user(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                args = event.message.message.split()
                user_to_unsilence_id = None
                if event.is_reply:
                    replied_msg = await event.get_reply_message()
                    user_to_unsilence_id = replied_msg.sender_id
                elif len(args) > 1 and args[1].isdigit():
                    user_to_unsilence_id = int(args[1])
                if user_to_unsilence_id in v["impolite"]:
                    v["impolite"].remove(user_to_unsilence_id)
                    with open("cloner.json", "w") as w:
                        json.dump(v, w)
                    await event.reply("**🧻user was removed from the vulgar list.**")
                else:
                    await event.reply("**🤷‍♂user in the list is not vulgar.**")

        @self.client.on(events.NewMessage(pattern="(?i)delallimpolite|پاکسازی لیست مبتذل"))
        async def clear_silence_list(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                v["impolite"] = []
                with open("cloner.json", "w") as w:
                    json.dump(v, w)
                await event.reply("**🧼The vulgar list was successfully cleared.**")

        @self.client.on(events.NewMessage(pattern="(?i)listimpolite|لیست مبتذل"))
        async def view_silence_list(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                silence_list = "\n".join(str(user_id)
                                         for user_id in v["impolite"])
                if silence_list:
                    await event.reply(f"**🦠Vulgar list**:\n {silence_list}")
                else:
                    await event.reply("**🤷‍♂user in the list is not vulgar.**")

        @self.client.on(events.NewMessage(incoming=True))
        async def delete_silenced_messages(event):
            sender_id = event.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["mute"]:
                await event.delete()

        @self.client.on(events.NewMessage(pattern="join"))
        async def join(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    link = M.text.split(" ")[1]
                    m = check_telegram_link(link)
                    if m is None:
                        await M.reply("Link is invaild")
                        return
                    typ = m[0]
                    channel_id = m[1][0]
                    try:
                        if typ == "username_link" or typ == "profile_link":
                            await self.client(functions.channels.JoinChannelRequest(channel=str(channel_id)))# type: ignore
                        elif typ == "invite_link":
                            await self.client(functions.messages.ImportChatInviteRequest(hash=channel_id))
                        else:
                            return
                    except errors.rpcerrorlist.UserAlreadyParticipantError:
                        pass
                    await M.reply("**🗿Joined**")
                except errors.InviteHashExpiredError:
                    await M.reply("❗️**CODE ERROR**")
                except errors.UserAlreadyParticipantError:
                    await M.reply("❗️**CODE ERROR**")

        @self.client.on(events.NewMessage(pattern="(?i)settime"))
        async def times(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    settime = float(M.text.split(" ")[1])
                    if str(settime) != v["sleep"]:
                        v["sleep"] = str(settime)
                        with open("cloner.json", "w") as f:
                            json.dump(v, f)
                        await M.reply(f"⏱**Speed Set {settime} **")
                    else:
                        await M.reply("**⏱Registered**")
                except Exception:
                    await M.reply(format_exc())

        @self.client.on(events.NewMessage(pattern="(?i)setgp"))
        async def tar(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    setgp = M.text.split(" ")[1]
                    if str(setgp) != v["chat"]:
                        v["chat"] = str(setgp)
                        with open("cloner.json", "w") as f:
                            json.dump(v, f)
                        await M.reply(f"**🔗ID Set Successfully {setgp} **")
                    else:
                        await M.reply("**🔗Registered**")
                except ValueError:
                    await M.reply("**‼️ Please Error ID **")

        @self.client.on(events.NewMessage(pattern="(?i)id|ایدی|آیدی"))
        async def id(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                if M.reply_to_msg_id:
                    r_msg = await M.get_reply_message()
                    await M.reply("**👥 Gp ID** : `{}`\n**👤 User ID** : `{}`".format(str(M.chat_id), str(r_msg.sender_id)))
                else:
                    await M.reply("**👥 Gp ID** : `{}`".format(str(M.chat_id)))

        @self.client.on(events.NewMessage(pattern="(?i)start"))
        async def start(M):
            sender_id = M.sender_id
            v = json.load(open("cloner.json"))
            if sender_id in v["admin"] + ADMINS:
                while True:
                    v = json.load(open("cloner.json"))
                    CHAT = int(v["chat"])
                    await asyncio.sleep(float(v["sleep"]))
                    if v["run"] == "0":
                        break
                    if v["mode"] == "text":
                        r_msg = 0
                        if M.reply_to_msg_id:
                            r_msgs = await M.get_reply_message()
                            r_msg = r_msgs.id
                        try:
                            fosh = random.choice(v["fosh"])
                            msg = fosh+"\n\n"
                            if v["tag"] == "on":
                                for id in v["id"]:
                                    msg += "[⸙](tg://user?id="+str(id)+") "
                            await self.client.send_message(int(CHAT), msg, reply_to=r_msg)
                        except Exception:
                            await self.client.send_message(int(CHAT), format_exc(), reply_to=r_msg)
                            break

                    elif v["mode"] == "for":
                        try:
                            riply_id = v["id_msg"]
                            from_id = v["from_id"]
                            await self.client.forward_messages(int(v["chat"]), riply_id, from_id)
                        except Exception as h:
                            await M.reply("**❗ Is The error**")
                            break
                    elif v["mode"] == "media":
                        try:
                            riply_id = v["id_msg"]
                            from_id = v["from_id"]

                            await send_file(int(v["chat"]), riply_id)
                        except MemoryError as h:
                            await M.reply("**❗ Is The error**")
                            break

        @self.client.on(events.NewMessage(pattern="(?i)fosh off"))
        async def stop(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                v["run"] = str(0)
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**💤Fosh Turned Off**")

        @self.client.on(events.NewMessage(pattern="(?i)fosh on"))
        async def stop1(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                v["run"] = str(1)
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**🌪Fosh Turned On**")

        @self.client.on(events.NewMessage(pattern="(?i)addfosh"))
        async def save(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    name = M.text.split(" ", maxsplit=1)[1]
                    v["fosh"] = v["fosh"] + [name]
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                    await M.reply("**🗂Add Successfully**")
                except AttributeError:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)setid"))
        async def save1(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                name = M.text[6:].strip().split()
                v["id"].clear()
                for n in name:
                    v["id"].append(n)
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**🔖Id Added**")

        @self.client.on(events.NewMessage(pattern="(?i)tag"))
        async def save2(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                name = M.text.split(" ")[1]
                if name == "on" or name == "off":
                    v["tag"] = str(name)
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                    await M.reply(f"**🔖Tag Is {name}**")

        @self.client.on(events.NewMessage(pattern="(?i)delallfosh"))
        async def delete(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    v["fosh"] = []
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                    await M.reply("**🗑Delete Successfully**")
                except AttributeError:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)left"))
        async def left_gap(M):
            sender_id = M.sender_id
            left_url = M.text.split(" ")[1]
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    m = check_telegram_link(left_url)
                    if m is None:
                        await M.reply("Link is invaild")
                        return
                    typ = m[0]
                    channel_id = m[1][0]
                    if typ == "invite_link":
                        result = await self.client(functions.messages.CheckChatInviteRequest(hash=channel_id))
                        if isinstance(result, types.ChatInviteAlready):
                            channel_id = result.chat.id
                    channel = await self.client.get_entity(channel_id)
                    if isinstance(channel, types.Chat) or isinstance(channel, types.Channel):
                        await self.client.delete_dialog(channel.id)
                    await M.reply("**🗿Lefted**")

                except Exception as e:
                    await M.reply(e)

        @self.client.on(events.NewMessage(pattern="(?i)mode"))
        async def mode11(M):
            sender_id = M.sender_id
            mode = M.text.split(" ")[1]
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    if mode in ["for", "text", "media"]:
                        v["mode"] = mode
                        with open("cloner.json", "w") as f:
                            json.dump(v, f)
                        await M.reply(f"**⚙Status to {mode} changed**")
                    else:
                        await M.reply("کصشرا چیه میفرستی")

                except Exception:
                    await M.reply("مشکل در  ربات")

        @self.client.on(events.NewMessage(pattern="(?i)setfor"))
        async def setfor(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                from_id = M.chat_id
                riply_id = M.reply_to_msg_id
                v["id_msg"] = riply_id
                v["from_id"] = from_id
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**📎The Desired Post Has Been Set**")

        @self.client.on(events.NewMessage(pattern="(?i)name"))
        async def name(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    name = M.text.split(" ", maxsplit=1)[1]
                    await self.client(functions.account.UpdateProfileRequest(first_name=name))
                    await M.reply(f"**Name To {name} Edited ✅**")
                except Exception:
                    await M.reply("**Please Enter A Name**")

        @self.client.on(events.NewMessage(pattern="(?i)bio"))
        async def bio(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    bio = M.text.split(" ", maxsplit=1)[1]
                    await self.client(functions.account.UpdateProfileRequest(about=bio))
                    await M.reply(f"** Name To {bio} Edited ✅**")
                except Exception:
                    await M.reply("** Please Enter A Bio**")

        @self.client.on(events.NewMessage(pattern="(?i)profile"))
        async def prof(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    reply = await M.get_reply_message()
                    x = await reply.download_media()
                    await self.client(functions.photos.UploadProfilePhotoRequest(
                        fallback=False,
                        file=await self.client.upload_file(x)))
                    await M.reply("**Profile Edited ✅**")
                except AttributeError:
                    await M.reply("** Please Reply To Photo**")

        @self.client.on(events.NewMessage(pattern="(?i)admin"))
        async def admin(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in ADMINS:
                id_Admin = M.text.split(" ")[1]
                v["admin"] = v["admin"] + [int(id_Admin)]
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**🫂Id Admin Add True**")

        @self.client.on(events.NewMessage(pattern="(?i)delalladmin"))
        async def delalladmin1(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in ADMINS:
                v["admin"] = [1]
                with open("cloner.json", "w") as f:
                    json.dump(v, f)
                await M.reply("**🗑Delete All Admins List**")

        @self.client.on(events.NewMessage(pattern="(?i)adminlist"))
        async def delalladmin(M):
            sender_id = M.sender_id
            if sender_id in ADMINS:
                all_admin = [i for i in open("admin.txt")]
                admins = ""
                for i in all_admin:
                    admins += i+"\n"
                await M.reply(f"**🗣All List Admin \n {str(admins)} **")

        @self.client.on(events.NewMessage(pattern="(?i)alldelprofile"))
        async def none(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                self.client.get_me
                me = await self.client(functions.users.GetFullUserRequest(types.InputUserSelf()))
                profile_pic = me.full_user.profile_photo
                while me.full_user.profile_photo:
                    await self.client(functions.photos.DeletePhotosRequest([profile_pic]))
                    me = await self.client(functions.users.GetFullUserRequest(types.InputUserSelf()))
                    profile_pic = me.full_user.profile_photo
                await M.reply("**🗑️ All Profile Deleted **")

        @self.client.on(events.NewMessage(pattern="(?i)addenemy"))
        async def enemy2(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    fromid = None
                    args = M.message.message.split()
                    if M.is_reply:
                        replied_msg = await M.get_reply_message()
                        fromid = replied_msg.sender_id
                    elif len(args) > 1 and args[1].isdigit():
                        fromid = int(args[1])
                    if fromid not in v["enemys"]:
                        v["enemys"].append(fromid)
                        with open("cloner.json", "w") as f:
                            json.dump(v, f)
                        await M.reply(f"⚔**Enemy Set {fromid} **")
                except Exception as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)answer-enemy"))
        async def enemy(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    times = M.text.split(" ")[1]
                    v["answer"] = int(times)
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                    await M.reply(f"😈**Count Set {times} **")
                except Exception as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)delenemy"))
        async def delenemy(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    fromid = None
                    args = M.message.message.split()
                    if M.is_reply:
                        replied_msg = await M.get_reply_message()
                        fromid = replied_msg.sender_id
                    elif len(args) > 1 and args[1].isdigit():
                        fromid = int(args[1])
                    with open("cloner.json") as r:
                        v = json.load(r)
                    if fromid in v["enemys"]:
                        v["enemys"].remove(fromid)
                        with open("cloner.json", "w") as f:
                            json.dump(v, f)
                        await M.reply(f"⚔**Enemy Deleted {fromid} **")
                except Exception as e:
                    await M.reply("**❗ Is The error**")
        data = {}

        @self.client.on(events.NewMessage(outgoing=False))
        async def enemmy(M):
            if Date_Expire < int(datetime.now().strftime("%Y%m%d")):
                for idz in ADMINS:
                    await self.client.send_message(int(idz), "تاریخ انقضای ربات تمام شد")
                self.client.disconnect()
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
                # and not sender_id in v["admin"] + ADMINS
            if sender_id in v["enemys"] and int(M.chat_id) == int(v['chat']):
                try:
                    if data.get(sender_id):
                        d = data[sender_id]
                        if not d["count"] >= v["answer"]:
                            if v["mode"] == "media":
                                await send_file(sender_id, M.id)
                            else:
                                await asyncio.sleep(float(v["sleep"]))
                                await M.reply(random.choice(v["fosh"]))
                            d["count"] = d["count"]+1
                        else:
                            if d["time"] + 60 < time.time():
                                d["time"] = time.time()
                                d["count"] = 0
                    else:
                        data[sender_id] = {"time": time.time(), "count": 1}
                        if v["mode"] == "media":
                            await send_file(sender_id, M.id)
                        else:
                            await asyncio.sleep(float(v["sleep"]))
                            await M.reply(random.choice(v["fosh"]))
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                except:
                    pass
            if sender_id in v["impolite"]:
                print(M.media)
                if M.media:
                    await self.client.delete_messages(sender_id, M.id)

        @self.client.on(events.NewMessage(pattern="(?i)delallenemy"))
        async def delallenemy(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    v["enemys"].clear()
                    with open("cloner.json", "w") as f:
                        json.dump(v, f)
                    await M.reply("🗑**Enemy List Cleared **")
                except MemoryError as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)enemylist"))
        async def enemylist2(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    tx = "📛 **Enemy List:**\n"
                    for id in v["enemys"]:
                        tx += f"•> `{id}`\n"
                    await M.reply(tx)
                except Exception as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)addmedia"))
        async def addmedia(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    reply = await M.get_reply_message()
                    if reply:
                        file = converter(reply)
                        if file["photo"]:
                            img = "img"
                        else:
                            img = "noimg"
                        file = file["result"]
                        if add_data((int(file.id), int(file.access_hash), file.file_reference, img)):
                            await M.reply("**🏖Add Successfully**")

                except Exception as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)delallmedia"))
        async def enemylist(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                try:
                    os.remove("db.db")
                    conn = sqlite3.connect("db.db")
                    await M.reply("**🗑Delete Successfully**")
                except Exception as e:
                    await M.reply("**❗ Is The error**")

        @self.client.on(events.NewMessage(pattern="(?i)help|راهنما"))
        async def help(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                load_avg = os.getloadavg()
                system_load_15min = load_avg[2]
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂  با ارسال دستور زیر از وضعیت ربات مطلع شوید. \n‎⇝ `status`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر راهنمای عمومی را باز کنید.\n‎⇝ `1help`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر راهنمای ست انمی را باز کنید.\n‎⇝ `2help`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر راهنمای پروفایل را باز کنید.\n‎⇝ `3help`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر راهنمای ادمین کردن را باز کنید.\n‎⇝ `4help`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر راهنمای مدیریت گروه را باز کنید.\n‎⇝ `5help`\n╍╍╍╍╍╍╍╍╍╍╍╍\n"
                              f"CPULoad : {system_load_15min}\nsupport : self mester")

        @self.client.on(events.NewMessage(pattern="(?i)1help"))
        async def help1(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر فوش مورد نظر خود را به اتکر اضافه کنید.\n‎⇝ `addfosh`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر تمام فوش های اضافه شده به اتکر را پاک کنید. \n‎⇝ `delallfosh`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر رسانه مورد نظر خود را به اتکر اضافه کنید. \n‎⇝ `addmedia`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر تمام رسانه های اضافه شده به اتکر را پاک کنید. \n‎⇝ `delallmedia`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر سرعت ارسال فوش (هم سرعت اسپم زدن هم سرعت ست انمی) را به ثانیه تنظیم کنید. \n‎⇝ `settime` (0.1~999)\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر ایدی عددی دشمن و گروه را دریافت کنید. \n‎⇝ `id`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر کاربر مورد نظر را برای منشن تنظیم کنید. \n‎⇝ `setid`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر گروه را برای ارسال فوش تنظیم کنید. \n‎⇝ `setgp`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر پست مورد نظر را برای فوروارد کردن ست کنید. \n‎⇝ `setfor`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر منشن کردن دشمن را خاموش روشن کنید. \n‎⇝ `tag` onیاoff\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر ارسال فوش را روشن و خاموش کنید. \n‎⇝ `fosh` onیاoff\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر بعد از fosh on ارسال فوش را شروع کنید. \n‎⇝ `start`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر مود ارسال پیام رو تغییر دهید.(سه مود داری تکست عادی و فوروارد و رسانه) \n‎⇝ `mode` textیاforیاmedia\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده دستور زیر اتکر رو جوین گروه مورد نظر کنید. \n‎⇝ `join`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر اتکر را از گروه مورد نظر خارج کنید. \n‎⇝ `left`\n╍╍╍╍╍╍╍╍╍╍╍╍\nsupport : self mester")

        @self.client.on(events.NewMessage(pattern="(?i)2help"))
        async def help2(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را به لیست دشمنان اضافه کنید. \n‎⇝ `addenemy`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را از لیست دشمنان حذف کنید. \n‎⇝ `delenemy`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر لیست دشمنان را پاکسازی کنید. \n‎⇝ `delallenemy`\n╍╍╍╍╍╍╍╍╍╍╍╍\nبا ارسال دستور زیر لیست دشمنان را مشاهده کنید. \n‎⇝ `enemylist`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ارسال دستور زیر تنظیم کنید که ربات در یک دقیقه چندبار جواب دشمن رو بده. \n⇝ `answer-enemy` (1~9999)\n╍╍╍╍╍╍╍╍╍╍╍╍\nsupport : self mester")

        @self.client.on(events.NewMessage(pattern="(?i)3help"))
        async def help3(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر اسم اکانت را عوض کنید. \n‎⇝ `name`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر بیو اکانت را عوض کنید. \n‎⇝` bio`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر پروف اکانت را عوض کنید. \n‎⇝ `profile`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر تمام پروفایل های اکانت را پاک کنید. \n‎⇝ `alldelprofile`\n╍╍╍╍╍╍╍╍╍╍╍╍\nsupport : self mester")

        @self.client.on(events.NewMessage(pattern="(?i)4help"))
        async def help4(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر ادمین جدید اضافه کنید به اتکر. \n‎⇝ `admin`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر ادمین مورد نظر را حذف کنید. \n‎⇝ `deladmin`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر تمام ادمین ها را حذف کنید. \n‎⇝ `delalladmin`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با استفاده از دستور زیر لیست ادمین ها را مشاهده کنید. \n‎⇝ `adminlist`\n╍╍╍╍╍╍╍╍╍╍╍╍\nsupport : self mester")

        @self.client.on(events.NewMessage(pattern="(?i)5help"))
        async def help5(M):
            sender_id = M.sender_id
            with open("cloner.json") as r:
                v = json.load(r)
            if sender_id in v["admin"] + ADMINS:
                await M.reply("✂️ راهنمای اتکر ورژن 6.9\n⇝help attacker 𝐕 ⁶\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را به لیست سکوت اضافه کنید. \n‎⇝ `mute`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را از لیست سکوت حذف کنید. \n‎⇝ `unmute`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر لیست سکوت را پاکسازی کنید. \n‎⇝ `unmuteall`\n╍╍╍╍╍╍╍╍╍╍╍╍\nبا ارسال دستور زیر لیست سکوت را مشاهده کنید. \n‎⇝ `listmute`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را به لیست مبتذل اضافه کنید. \n‎⇝ `impolite`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر کاربر مورد نظر را از لیست مبتذل حذف کنید. \n‎⇝ `delimpolite`\n╍╍╍╍╍╍╍╍╍╍╍╍\n◂ با ریپلای و ارسال دستور زیر لیست مبتذل را پاکسازی کنید. \n‎⇝ `delallimpolite`\n╍╍╍╍╍╍╍╍╍╍╍╍\nبا ارسال دستور زیر لیست مبتذل را مشاهده کنید. \n‎⇝ `listimpolite`\n╍╍╍╍╍╍╍╍╍╍╍╍\nsupport : self mester")

        self.client.run_until_disconnected()


Main().bot()
