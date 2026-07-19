import httpx
import asyncio
from utils.logger import setup_logger

logger = setup_logger()

async def check_url(client, url):
    try:
        # Prioritaskan cek HTTPS, karena nyatanya prioritas dia bukan cuma kamu doang
        target_url = f"https://{url}"
        # follow_redirects=True buat ngikutin alur kalau misal di-redirect ke login page
        response = await client.get(target_url, timeout=10.0, follow_redirects=True)
        return url, response.status_code
    except httpx.RequestError:
        # Kalau HTTPS gagal, coba HTTP ajah
        try:
            target_url = f"http://{url}"
            response = await client.get(target_url, timeout=10.0, follow_redirects=True)
            return url, response.status_code
        except httpx.RequestError:
            # Kalau dua-duanya gagal, berarti servernya mungkin mati, atau mungkin perasaan kalian yang udah sama-sama mati
            return url, 0

async def probe_subdomains(subdomains):
    logger.info(f"Starting HTTP probing for {len(subdomains)} subdomains...")
    results = {'live': [], 'dead': []}
    limits = httpx.Limits(max_connections=50, max_keepalive_connections=10)
    async with httpx.AsyncClient(limits=limits, verify=False) as client:
        tasks = [check_url(client, sub) for sub in subdomains]
        responses = await asyncio.gather(*tasks)
        
        for url, status in responses:
            if status > 0:
                results['live'].append({'url': url, 'status': status})
                logger.debug(f"[LIVE] {url} - Status: {status}")
            else:
                results['dead'].append(url)
                
    logger.info(f"Probing completed. Found {len(results['live'])} live targets and {len(results['dead'])} dead targets.")
    return results