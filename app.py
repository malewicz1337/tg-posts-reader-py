import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import InputPhotoFileLocation
from telethon.utils import pack_bot_file_id

from sel_scraper import get_telegram_image_url

load_dotenv()

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
phone_number = os.environ["PHONE_NUMBER"]
channel_username = os.environ["CHANNEL_USERNAME"]

client = TelegramClient("session", api_id, api_hash)


async def main():
    async with TelegramClient("session", api_id, api_hash) as client:
        channel_entity = await client.get_entity(channel_username)
        all_messages = []
        total_count_limit = 10

        async for message in client.iter_messages(
            channel_entity, limit=total_count_limit
        ):
            all_messages.append(message.to_dict())
            print(f"Total Messages: {len(all_messages)}")

            if len(all_messages) >= total_count_limit:
                break

        total_messages = len(all_messages)
        print(f"Total messages retrieved: {total_messages}")
        print("Message structure:", all_messages[0].keys())

        for message in all_messages:
            print(f"Message ID: {message.get('id', 'Unknown ID')}")

            if message.get("message"):
                print(f"Text: {message['message']}")

            media = message.get("media", {})
            if isinstance(media, dict):
                media_type = media.get("_", "Unknown media type")
                print(f"Media Type: {media_type}")

                if media_type == "MessageMediaPhoto":
                    print("Photo detected")
                    photo = media.get("photo", {})
                    if isinstance(photo, dict):
                        photo_id = photo.get("id")
                        photo_access_hash = photo.get("access_hash")
                        photo_file_reference = photo.get("file_reference")
                        print(f"Photo ID: {photo_id}")
                        print(f"Access Hash: {photo_access_hash}")
                        print(f"File Reference: {photo_file_reference}")

                        file_id = pack_bot_file_id(
                            InputPhotoFileLocation(
                                id=photo_id,
                                access_hash=photo_access_hash,
                                file_reference=photo_file_reference,
                                thumb_size="x",
                            )
                        )
                        print(f"File ID: {file_id}")

                        chat_id = message.get("peer_id", {}).get("channel_id")
                        message_id = message.get("id")
                        if chat_id and message_id:
                            links = {
                                "Deep Link": f"https://t.me/c/{chat_id}/{message_id}",
                                "Public Link": f"https://t.me/{channel_username}/{message_id}",
                            }
                            for link_type, link in links.items():
                                print(f"{link_type}: {link}")

                            print(
                                f"Image CDN URL: {get_telegram_image_url(links['Public Link'])}"
                            )
                        else:
                            print(
                                "Couldn't create links: chat_id or message_id not found"
                            )
                    else:
                        print("Photo information not found in the expected structure")

            action = message.get("action")
            if action:
                action_type = (
                    action.get("_", "Unknown action type")
                    if isinstance(action, dict)
                    else action
                )
                print(f"Action: {action_type}")

            print("-" * 50)


asyncio.run(main())
