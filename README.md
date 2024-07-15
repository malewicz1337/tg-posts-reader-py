# Telegram Channel History Scraper

This script uses the Telethon library to scrape messages from a specified Telegram channel and print out the messages' content.

## Configuration

Replace the placeholder values in the script with your actual credentials:
``` python
api_id = "<telegram-api-id>"
api_hash = "<telegram-api-hash>"
phone_number = "<phone-number>"
channel_username = "<channel-username>"
```

## Output

The script will print the content of the messages retrieved from the specified Telegram channel. The output includes:

- Text messages
- Media messages
- Action messages

## Notes

The script fetches messages in batches of 100 until it reaches a total limit of 1000 messages.
You can adjust the `limit` and `total_count_limit` variables in the script according to your needs.

## License
This project is open source and available under the [MIT License](LICENSE).
