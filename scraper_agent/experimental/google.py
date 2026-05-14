"""
Experimental Google scraper.
Currently blocked by CAPTCHA detection.
Needs stealth + anti-bot improvements later.
"""

from googlesearch import search
from shared.logger import logger
import time
import random


def google_search(query, num_results=10):
    """
    Search Google and return results
    """

    logger.info(f"Starting Google search for: {query}")

    results = []

    try:
        search_results = search(
            query,
            num_results=num_results,
            lang="en"
        )

        for url in search_results:

            logger.info(f"Found URL: {url}")

            results.append({
                "query": query,
                "url": url,
                "source": "google"
            })

            # Random delay
            time.sleep(random.uniform(1, 3))

    except Exception as e:
        logger.error(f"Google search failed: {e}")

    logger.info(f"Finished search. Total results: {len(results)}")

    return results