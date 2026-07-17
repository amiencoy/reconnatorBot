import httpx
from utils.logger import setup_logger

logger = setup_logger()

def fetch_subdomains_otx(domain):
    logger.info(f"Finding available subdomain for {domain} taken from AlienVault OTX...")
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    
    subdomains = set()
    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if 'passive_dns' in data:
                for entry in data['passive_dns']:
                    hostname = entry.get('hostname')
                    if hostname and hostname.endswith(domain):
                        clean_host = hostname.lstrip('*.')
                        subdomains.add(clean_host)
                        
        logger.info(f"Found {len(subdomains)} unique subdomains from OTX.")
        return list(subdomains)
        
    except Exception as e:
        logger.error(f"Failed to retrieve data from AlienVault OTX: {e}")
        return []