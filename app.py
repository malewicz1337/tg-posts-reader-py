import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPhotoFileLocation
from telethon.utils import pack_bot_file_id

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
channel_username = os.getenv("CHANNEL_USERNAME")

client = TelegramClient("session", api_id, api_hash)


async def main():
    client.start()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input("Enter the code: "))
        except Exception as e:
            print(e)
            await client.sign_in(password=input("Password: "))

    channel_entity = await client.get_entity(channel_username)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 10

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(
            GetHistoryRequest(
                peer=channel_entity,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit is not None and total_messages >= total_count_limit:
            break

    print("Total messages:", total_messages)
    print("Message structure:", all_messages[0].keys())

    for message in all_messages:
        print(f"Message ID: {message.get('id', 'Unknown ID')}")

        if "message" in message and message["message"]:
            print(f"Text: {message['message']}")

        if "media" in message:
            media = message["media"]
            if isinstance(media, dict):
                media_type = media.get("_", "Unknown media type")
                print(f"Media Type: {media_type}")

                if media_type == "MessageMediaPhoto":
                    print("Photo detected")
                    if "photo" in media and isinstance(media["photo"], dict):
                        photo = media["photo"]
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
                            deep_link = f"https://t.me/c/{chat_id}/{message_id}"
                            print(f"Telegram Deep Link: {deep_link}")
                            public_link = f"https://t.me/c/{chat_id}/{message_id}"
                            print(f"Public Telegram Link: {public_link}")
                            user_friendly_link = (
                                f"https://t.me/{channel_username}/{message_id}"
                            )
                            print(f"User-friendly Telegram Link: {user_friendly_link}")
                            print(get_image_url(user_friendly_link))
                        else:
                            print(
                                "Couldn't create deep link: chat_id or message_id not found"
                            )

                    else:
                        print("Photo information not found in the expected structure")

        if "action" in message:
            if isinstance(message["action"], dict):
                action_type = message["action"].get("_", "Unknown action type")
                print(f"Action: {action_type}")
            else:
                print(f"Action: {message['action']}")

        print("-" * 50)


with client:
    client.loop.run_until_complete(main())
