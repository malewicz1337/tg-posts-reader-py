from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

api_id = "<telegram-api-id>"
api_hash = "<telegram-api-hash>"
phone_number = "<phone-number>"
channel_username = "<channel-username>"

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
    total_count_limit = 1000

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
        if "message" in message:
            print(f"Text: {message['message']}")
        elif "media" in message:
            print(f"Media: {message['media'].get('_', 'Unknown media type')}")
        elif "action" in message:
            print(f"Action: {message['action'].get('_', 'Unknown action type')}")
        else:
            print("This update contains neither text nor media.")
        print("-" * 50)


with client:
    client.loop.run_until_complete(main())
