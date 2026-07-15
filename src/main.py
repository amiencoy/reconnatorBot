import os
import argparse
from modules.crtsh_fetcher import fetch_subdomains
from modules.notifier import send_telegram_alert
from utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Reconnator - Cloud-Native Recon Bot")
    parser.add_argument("-t", "--target", required=True, help="Target domain (example: hackerone.com)")
    args = parser.parse_args()

    domain = args.target
    logger.info(f"Starting Reconnator for target: {domain}")

    # 1. Fetcher subdomain doang kok, ga lebih
    subdomains = fetch_subdomains(domain)
    
    if not subdomains:
        logger.info("No subdomains found or an error occurred.")
        return

    # 2. Format notif, biar bersaing sama notif dari doi
    message = f"🔍 *Reconnator Report*\n*Target:* {domain}\n*Total Subdomains:* {len(subdomains)}\n\n"
    preview_limit = 10
    for sub in subdomains[:preview_limit]:
        message += f"- `{sub}`\n"
        
    if len(subdomains) > preview_limit:
        message += f"\n_...and {len(subdomains) - preview_limit} more subdomains._"

    # 3. Kirim notif, tapi kalo ada tokennya, kalo ga ada ya udah, diem doang
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    send_telegram_alert(telegram_token, telegram_chat_id, message)
    logger.info("Execution of Reconnator completed.")

if __name__ == "__main__":
    main()