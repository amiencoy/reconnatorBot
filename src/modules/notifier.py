import os
import httpx
from utils.logger import setup_logger

logger = setup_logger()

def send_telegram_message(target, live_targets, dead_count):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("Telegram credentials are incomplete. Skipping notification sending.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    message = (
        f"🕵️‍♂️ *Reconnator Alert*\n\n"
        f"🎯 *Target:* `{target}`\n"
        f"✅ *Live Assets:* {len(live_targets)}\n"
        f"💀 *Dead Assets:* {dead_count}\n\n"
    )

    if live_targets:
        message += "*Top 5 Live Targets:*\n"
        for item in live_targets[:5]:
            message += f"• `{item['url']}` [HTTP {item['status']}]\n"
            
        if len(live_targets) > 5:
            message += f"• ...and {len(live_targets) - 5} more.\n"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        # Pake httpx sinkronus karena pengiriman notif ini berjalan di akhir eksekusi
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            logger.info("Telegram notification sent successfully.")
            return True
    except httpx.RequestError as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False