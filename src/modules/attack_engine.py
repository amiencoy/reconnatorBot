import asyncio
import json
import logging

logger = logging.getLogger(__name__)

async def run_nuclei(target: str) -> list:
    """
    Executes Nuclei via Ephemeral Docker Container asynchronously.
    Optimized for speed: No updates, limited high-value templates, increased concurrency.
    """
    logger.info(f"Initiating OPTIMIZED containerized Nuclei strike on {target}...")
    
    cmd = [
        "docker", "run", "--rm", 
        "projectdiscovery/nuclei:latest", 
        "-u", target, 
        "-silent", 
        "-jsonl",
        "-duc",
        "-c", "50",
        "-t", "cves,vulnerabilities,misconfiguration,exposed-panels"
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0 and stderr:
            logger.warning(f"Nuclei stderr: {stderr.decode().strip()}")
            
        results = []
        for line in stdout.decode().splitlines():
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                    
        logger.info(f"Nuclei strike complete. Found {len(results)} issues.")
        return results

    except Exception as e:
        logger.error(f"Failed to execute containerized Nuclei: {e}")
        return []