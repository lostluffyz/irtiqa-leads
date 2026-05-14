from shared.logger import logger
from researcher_agent.config.keywords import (
    BUSINESS_KEYWORDS,
    SCALING_SIGNALS,
    PAIN_POINT_KEYWORDS,
    AUTOMATION_KEYWORDS,
    HIGH_VALUE_SIGNALS
)

# =========================
# KEYWORD MATCHER
# =========================

def match_keywords(text):

    logger.info(
        "Running keyword matching"
    )

    text = text.lower()

    matched_business = []

    matched_scaling = []

    matched_pain = []

    matched_automation = []

    # -------------------------
    # BUSINESS KEYWORDS
    # -------------------------

    for keyword in BUSINESS_KEYWORDS:

        if keyword in text:

            matched_business.append(
                keyword
            )

    # -------------------------
    # SCALING SIGNALS
    # -------------------------

    for keyword in SCALING_SIGNALS:

        if keyword in text:

            matched_scaling.append(
                keyword
            )

    # -------------------------
    # PAIN POINT KEYWORDS
    # -------------------------

    for keyword in PAIN_POINT_KEYWORDS:

        if keyword in text:

            matched_pain.append(
                keyword
            )

    # -------------------------
    # AUTOMATION SIGNALS
    # -------------------------

    for keyword in AUTOMATION_KEYWORDS:

        if keyword in text:

            matched_automation.append(
                keyword
            )

    matched_high_value = []

    for keyword in HIGH_VALUE_SIGNALS:

        if keyword in text:

            matched_high_value.append(
            keyword
        )

    result = {

        "business_keywords":
            list(set(matched_business)),

        "scaling_signals":
            list(set(matched_scaling)),

        "pain_keywords":
            list(set(matched_pain)),

        "automation_keywords":
            list(set(matched_automation)),
        "high_value_signals":
            list(set(matched_high_value))
    }

    logger.info(
        f"Matched "
        f"{len(matched_business)} business "
        f"keywords"
    )

    return result


# =========================
# TEST
# =========================

if __name__ == "__main__":

    sample_text = """

    We are a digital marketing agency
    helping SaaS startups scale fast.

    Our growing sales team uses
    HubSpot and automation systems
    to improve workflow efficiency.

    """

    result = match_keywords(
        sample_text
    )

    print(result)