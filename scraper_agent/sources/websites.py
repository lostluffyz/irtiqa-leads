import httpx
from shared.text_cleaner import clean_text
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from shared.logger import logger
import re


# =========================
# CONTACT INFO EXTRACTION
# =========================

def extract_contact_info(text):

    email_pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    phone_pattern = r"\+?\d[\d\s\-\(\)]{8,}\d"

    emails = re.findall(email_pattern, text)

    phones = re.findall(phone_pattern, text)

    cleaned_phones = []

    for phone in phones:

        digits_only = re.sub(r"\D", "", phone)

        if 10 <= len(digits_only) <= 13:

            if len(set(digits_only)) > 3:

                cleaned_phones.append(phone.strip())

    return {
        "emails": list(set(emails)),
        "phones": list(set(cleaned_phones))
    }


# =========================
# INTERNAL PAGE SCRAPER
# =========================

def scrape_internal_page(url, headers):

    try:

        logger.info(f"Scraping internal page: {url}")

        response = httpx.get(
            url,
            headers=headers,
            timeout=10,
            follow_redirects=True
        )

        soup = BeautifulSoup(response.text, "lxml")

        visible_text = soup.get_text(separator=" ").lower()

        return extract_contact_info(visible_text)

    except Exception as e:

        logger.error(f"Failed scraping internal page {url}: {e}")

        return {
            "emails": [],
            "phones": []
        }


# =========================
# MAIN WEBSITE SCRAPER
# =========================

def scrape_website(url):

    logger.info(f"Scraping website: {url}")

    data = {
        "url": url,
        "title": None,
        "emails": [],
        "phones": [],
        "text": "",
        "internal_links": []
    }

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        response = httpx.get(
            url,
            headers=headers,
            timeout=15,
            follow_redirects=True
        )

        html = response.text

        soup = BeautifulSoup(html, "lxml")

        # =========================
        # FIND INTERNAL LINKS
        # =========================

        internal_links = []

        keywords = [
            "contact",
            "about",
            "team",
            "company"
        ]

        blocked_domains = [
            "linkedin.com",
            "youtube.com",
            "facebook.com",
            "twitter.com",
            "x.com",
            "instagram.com"
        ]

        for link in soup.find_all("a", href=True):

            href = link["href"].lower()

            full_url = urljoin(url, href)

            # Skip blocked domains
            should_skip = False

            for blocked in blocked_domains:

                if blocked in full_url:

                    should_skip = True
                    break

            if should_skip:
                continue

             # Keep useful internal pages only
            for keyword in keywords:

                if keyword in href:

                    internal_links.append(full_url)

        internal_links = list(set(internal_links))

        # =========================
        # EXTRACT TITLE
        # =========================

        if soup.title:
            data["title"] = soup.title.text.strip()

        # =========================
        # SMART TEXT EXTRACTION
        # =========================

        extracted_sections = []

        # -------------------------
        # HEADINGS
        # -------------------------

        for tag in soup.find_all([

            "h1",
            "h2",
            "h3"
        ]):

            text = tag.get_text(
                strip=True
            )

            text = clean_text(text)

            if 15 < len(text) < 300:

                extracted_sections.append(
                    text
                )

        # -------------------------
        # IMPORTANT BUSINESS SECTIONS
        # -------------------------

        important_keywords = [

            "about",
            "services",
            "solutions",
            "what we do",
            "who we are",
            "our mission",
            "company",
            "agency"
        ]

        for tag in soup.find_all([

            "section",
            "div"
        ]):

            section_text = tag.get_text(

                separator=" ",
                strip=True
            )

            cleaned_section = clean_text(
                section_text
            )

            lower_text = cleaned_section.lower()

            for keyword in important_keywords:

                if keyword in lower_text:

                    if 80 < len(cleaned_section) < 1200:

                        extracted_sections.append(
                            cleaned_section
                        )

                        break

        # -------------------------
        # META DESCRIPTION
        # -------------------------

        meta_description = soup.find(

            "meta",

            attrs={
                "name": "description"
            }
        )

        if meta_description:

            content = meta_description.get(
                "content",
                ""
            )

            content = clean_text(content)

            if len(content) > 20:

                extracted_sections.append(
                    content
                )

        # -------------------------
        # FINAL CLEAN TEXT
        # -------------------------

        visible_text = "\n".join(

            list(set(extracted_sections))
        )

        visible_text = visible_text.lower()

        data["text"] = visible_text[:4000]

        # =========================
        # HOMEPAGE CONTACT INFO
        # =========================

        contact_info = extract_contact_info(visible_text)

        all_emails = set(contact_info["emails"])

        all_phones = set(contact_info["phones"])

        # =========================
        # SCRAPE INTERNAL PAGES
        # =========================

        for internal_url in internal_links:

            internal_data = scrape_internal_page(
                internal_url,
                headers
            )

            all_emails.update(internal_data["emails"])

            all_phones.update(internal_data["phones"])

        # =========================
        # FINAL MERGED RESULTS
        # =========================

        data["emails"] = list(all_emails)

        data["phones"] = list(all_phones)

        # =========================
        # LOGGING
        # =========================

        logger.info(f"Website title: {data['title']}")
        logger.info(f"Found {len(data['emails'])} emails")
        logger.info(f"Found {len(data['phones'])} phone numbers")
        logger.info(f"Found {len(data['internal_links'])} internal links")

    except Exception as e:

        logger.error(f"Website scraping failed: {e}")

    return data