from scraper_agent.sources.websites import scrape_website

from researcher_agent.classifiers.keyword_matcher import (
    match_keywords
)

from researcher_agent.classifiers.qualification_engine import (
    qualify_lead
)

from researcher_agent.classifiers.industry_classifier import (
    classify_industry
)

from researcher_agent.classifiers.pain_point_extractor import (
    extract_pain_points
)

from researcher_agent.classifiers.signal_scorer import (
    score_signals
)

from scorer_agent.scoring.numerical_scorer import (
    calculate_lead_score
)

from scorer_agent.message_generator.linkedin_message import (
    generate_linkedin_message
)

from database.inserts import (
    save_raw_lead,
    save_verified_lead
)

from researcher_agent.utils.context_selector import (
    select_relevant_context
)

from database.queries import (
    lead_exists
)

from shared.logger import logger


# =========================
# PROCESS SINGLE LEAD
# =========================

def process_lead(url):

    logger.info(
        f"Processing lead: {url}"
    )

    # =========================
    # DUPLICATE CHECK
    # =========================

    if lead_exists(url):

        logger.warning(
            f"Lead already exists: {url}"
        )

        return None

    # =========================
    # SCRAPE WEBSITE
    # =========================

    website_data = scrape_website(
        url
    )

    # =========================
    # VALIDATE SCRAPED DATA
    # =========================

    if not website_data.get("text"):

        logger.error(
            f"No website text found "
            f"for {url}"
        )

        return None

    # =========================
    # OPTIMIZED AI CONTEXT
    # =========================

    ai_context = select_relevant_context(

        website_data["text"]
    )

    # =========================
    # SAVE RAW LEAD
    # =========================

    raw_lead_id = save_raw_lead(
        website_data
    )

    logger.info(
        f"Saved raw lead ID: "
        f"{raw_lead_id}"
    )

    # =========================
    # KEYWORD MATCHING
    # =========================

    keyword_result = match_keywords(
        ai_context
    )

    # =========================
    # QUALIFICATION ENGINE
    # =========================

    qualification_result = qualify_lead(
        keyword_result
    )

    # =========================
    # INDUSTRY CLASSIFICATION
    # =========================

    industry_result = classify_industry(

        company_name=website_data["title"],

        description=ai_context,

        keyword_result=keyword_result,

        website_text=ai_context
    )

    # =========================
    # PAIN POINT EXTRACTION
    # =========================

    pain_result = extract_pain_points(

        website_data["title"],

        ai_context
    )

    # =========================
    # SIGNAL SCORING
    # =========================

    signal_result = score_signals(
        ai_context
    )

    # =========================
    # MERGE ENRICHED DATA
    # =========================

    enriched_lead = {

        **website_data,

        **keyword_result,

        **qualification_result,

        **industry_result,

        **pain_result,

        **signal_result
    }

    # =========================
    # LEAD SCORING
    # =========================

    scoring_result = calculate_lead_score(
        enriched_lead
    )

    enriched_lead.update(
        scoring_result
    )

    # =========================
    # OPTIMIZE OUTREACH CONTEXT
    # =========================

    outreach_context = {

        **enriched_lead,

        "text": ai_context
    }

    # =========================
    # GENERATE OUTREACH
    # =========================

    linkedin_message = generate_linkedin_message(
        outreach_context
    )

    enriched_lead[
        "linkedin_message"
    ] = linkedin_message

    # =========================
    # SAVE VERIFIED LEAD
    # =========================

    save_verified_lead(

        raw_lead_id,

        enriched_lead
    )

    logger.info(
        "Verified lead saved"
    )

    # =========================
    # FINAL OUTPUT
    # =========================

    print(
        "\n========== FINAL LEAD ==========\n"
    )

    print(enriched_lead)

    return enriched_lead


# =========================
# MAIN ENTRY
# =========================

if __name__ == "__main__":

    lead_urls = [

        "https://www.singlegrain.com",

        "https://neilpatel.com",

        "https://www.hawksem.com"
    ]

    all_results = []

    for url in lead_urls:

        try:

            result = process_lead(
                url
            )

            if result:

                all_results.append(
                    result
                )

        except Exception as e:

            logger.error(

                f"Failed processing "
                f"{url}: {e}"
            )

    print(

        f"\nProcessed "
        f"{len(all_results)} "
        f"leads successfully."
    )