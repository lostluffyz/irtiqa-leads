"""
Experimental Google scraper.
Currently blocked by CAPTCHA detection.
Needs stealth + anti-bot improvements later.
"""



from playwright.sync_api import sync_playwright
from shared.logger import logger
import time
import random


def google_search_playwright(query, num_results=5):

    logger.info(f"Starting Playwright Google search: {query}")

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Open Google
        page.goto("https://www.google.com")

        # Accept cookies if popup appears
        try:
            page.click("button:has-text('Accept all')", timeout=3000)
        except:
            pass

        # Search
        page.fill("textarea[name='q']", query)
        page.keyboard.press("Enter")

        # Wait for results
        page.wait_for_timeout(3000)

        # Extract links
        links = page.locator("a")

        count = 0

        for i in range(links.count()):

            href = links.nth(i).get_attribute("href")

            if href and href.startswith("http"):

                logger.info(f"Found URL: {href}")

                results.append({
                    "query": query,
                    "url": href,
                    "source": "google_playwright"
                })

                count += 1

            if count >= num_results:
                break

        time.sleep(random.uniform(1, 3))

        browser.close()

    logger.info(f"Finished search. Total results: {len(results)}")

    return results