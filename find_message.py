import asyncio
import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

load_dotenv()

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
phone_number = os.environ["PHONE_NUMBER"]
channel_username = os.environ["CHANNEL_USERNAME"]


async def main(post_link):
    async with TelegramClient("session", api_id, api_hash) as client:
        match = re.match(r"https://t\.me/([^/]+)/(\d+)", post_link)
        if not match:
            print("Invalid link format")
            return

        channel_username, message_id = match.groups()
        message_id = int(message_id)

        channel_entity = await client.get_entity(
            PeerChannel(int(channel_username))
            if channel_username.isdigit()
            else channel_username
        )

        message = await client.get_messages(channel_entity, ids=message_id)

        print(f"Message: {message}")


asyncio.run(main(""))
