import requests
import time
from utils.logger import setup_logger

logger = setup_logger()
def fetch_subdomains(domain, retries=3):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    logger.info(f"Finding any available subdomain for {domain} taken from crt.sh...")
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                data = response.json()
                subdomains = set()
                for entry in data:
                    name_val = entry.get('name_value', '')
                    if not name_val.startswith('*'):
                        for n in name_val.split('\n'):
                            subdomains.add(n.strip())         
                logger.info(f"Found {len(subdomains)} unique subdomains.")
                return sorted(list(subdomains))
            elif response.status_code in [502, 503, 504]:
                logger.warning(f"Attempt {attempt}/{retries}: crt.sh server down (HTTP {response.status_code}). Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logger.error(f"Failed to retrieve data. HTTP Status: {response.status_code}")
                break
        except requests.exceptions.ReadTimeout:
            logger.warning(f"Attempt {attempt}/{retries}: Connection to crt.sh timed out. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error occurred while contacting crt.sh: {e}")
            break
    logger.error("Failed to retrieve data from crt.sh after maximum retries.")
    return []