# Telegram Channel History Scraper

This script uses the Telethon library to scrape messages from a specified Telegram channel and print out the messages' content, including text, media, and action messages. It also retrieves and displays image URLs for photo messages.

## Prerequisites

Then edit the `.env` file and replace the placeholder values with your actual credentials:

- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `PHONE_NUMBER`: Your phone number associated with the Telegram account
- `CHANNEL_USERNAME`: The username of the Telegram channel you want to scrape

## Features

- Retrieves messages from a specified Telegram channel
- Handles text messages, media messages, and action messages
- For photo messages, it provides:
  - Photo ID
  - Access Hash
  - File Reference
  - File ID
  - Deep Link and Public Link to the message
  - CDN URL of the image (retrieved using Selenium)

## Configuration

You can adjust the following variables in `app.py` to modify the script's behavior:

- `total_count_limit`: The maximum number of messages to retrieve (default is 10)

## Output

The script will print detailed information for each message, including:

- Message ID
- Text content (if available)
- Media type and details (for media messages)
- Action type (for action messages)
- Links and CDN URL (for photo messages)

## Notes

- The script uses Selenium with Chrome in headless mode to scrape image URLs. Make sure you have Chrome installed on your system.
- The `ChromeDriver` is automatically managed by the `webdriver_manager` library.

## License

This project is open source and available under the [MIT License](LICENSE).
