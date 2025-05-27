import os
import random
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Load from environment
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Shayari loader
def get_random_shayari():
    try:
        with open("shayari.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return random.choice(lines)
    except:
        return "Subah ho gayi hai, uth ja bhai!"

# .gmtag command
@client.on(events.NewMessage(pattern=r"\.gmtag"))
async def good_morning_tag(event):
    if not event.is_group:
        return await event.reply("Sirf group mein kaam karta hai yeh command.")

    try:
        await event.delete()
    except:
        pass

    await event.respond("Shubh Prabhat! Ek ek karke sabko tag kiya ja raha hai...")

    participants = await client.get_participants(event.chat_id)
    
    for user in participants:
        if user.bot or user.deleted:
            continue
        name = user.first_name or "Friend"
        mention = f"[{name}](tg://user?id={user.id})"
        msg = f"**Good Morning!**\n{get_random_shayari()}\n{mention}"
        await client.send_message(event.chat_id, msg, parse_mode="md")
        await asyncio.sleep(2)  # 2 second delay

print("Bot ready hai!")
client.start()
client.run_until_disconnected()
