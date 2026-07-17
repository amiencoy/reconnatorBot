import argparse
import asyncio
import os
import urllib3
from dotenv import load_dotenv
from utils.logger import setup_logger
from modules.notifier import send_telegram_message
from modules.crtsh_fetcher import fetch_subdomains
from modules.otx_fetcher import fetch_subdomains_otx
from modules.http_prober import probe_subdomains

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Reconnator - Cloud-Native Recon Bot")
    parser.add_argument('--target', required=True, help="Target domain (e.g., hackerone.com)")
    args = parser.parse_args()

    target = args.target
    logger.info(f"Starting Reconnator for target: {target}")

    subdomains = fetch_subdomains(target)
    
    if not subdomains:
        logger.warning("crt.sh failed or returned empty results. Fallback to AlienVault OTX...")
        subdomains = fetch_subdomains_otx(target)
        
    if not subdomains:
        logger.error("All API sources failed or no subdomains found. Exiting.")
        return

    logger.info(f"Forwarding {len(subdomains)} subdomain to HTTP Prober...")
    probe_results = asyncio.run(probe_subdomains(subdomains))
    
    live_targets = probe_results.get('live', [])
    dead_targets = probe_results.get('dead', [])
    
    if live_targets:
        logger.info("=== Preview Live Targets ===")
        for item in live_targets[:5]:
            logger.info(f" -> {item['url']} [HTTP {item['status']}]")
        if len(live_targets) > 5:
            logger.info(f"    ... and {len(live_targets) - 5} other live targets.")
            
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        logger.warning("Telegram bot token or chat ID is not provided. Skipping Telegram alert...")
    else:
        logger.info(f"Sending Telegram notification for {len(live_targets)} targets alive...")
        send_telegram_message(target, live_targets, len(dead_targets))

    logger.info("Execution of Reconnator completed.")

if __name__ == "__main__":
    main()