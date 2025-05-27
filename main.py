import os
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Load environment variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Create Telegram client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Function to get a random shayari from file
def get_random_shayari():
    try:
        with open("shayari.txt", "r", encoding="utf-8") as f:
            shayari_list = [line.strip() for line in f if line.strip()]
            return random.choice(shayari_list)
    except Exception:
        return "Subah ho gayi hai dost!"

# Command: .gmtag
@client.on(events.NewMessage(pattern=r"\.gmtag"))
async def good_morning_tag(event):
    if not event.is_group:
        return await event.reply("Yeh command sirf group mein kaam karti hai.")

    await event.reply("Sabko Good Morning keh raha hoon... ruk jao thoda!")

    participants = await client.get_participants(event.chat_id)
    mentions = []
    for user in participants:
        if user.bot or user.deleted:
            continue
        name = user.first_name or "Friend"
        mention = f"[{name}](tg://user?id={user.id})"
        mentions.append(mention)

    chunk_size = 5
    for i in range(0, len(mentions), chunk_size):
        chunk = mentions[i:i+chunk_size]
        text = f"**Good Morning!**\n{get_random_shayari()}\n" + " ".join(chunk)
        await client.send_message(event.chat_id, text, parse_mode="md")

print("Bot Started!")
client.start()
client.run_until_disconnected()
