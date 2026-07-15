import requests
from utils.logger import setup_logger

logger = setup_logger()
def send_telegram_alert(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        logger.warning("Telegram bot token or chat ID is not provided. Skipping Telegram alert....")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("Notification sent successfully to Telegram!")
        else:
            logger.error(f"Failed to send notification. HTTP Status: {response.status_code}")
    except Exception as e:
        logger.error(f"Error occurred while sending Telegram alert: {e}")