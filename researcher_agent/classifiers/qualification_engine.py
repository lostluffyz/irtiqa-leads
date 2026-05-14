from shared.logger import logger


# =========================
# QUALIFICATION ENGINE
# =========================

def qualify_lead(keyword_data):

    logger.info(
        "Running qualification engine"
    )

    # -------------------------
    # EXTRACT SIGNALS
    # -------------------------

    business_keywords = keyword_data.get(
        "business_keywords",
        []
    )

    scaling_signals = keyword_data.get(
        "scaling_signals",
        []
    )

    pain_keywords = keyword_data.get(
        "pain_keywords",
        []
    )

    automation_keywords = keyword_data.get(
        "automation_keywords",
        []
    )

    high_value_signals = keyword_data.get(
        "high_value_signals",
        []
    )

    # -------------------------
    # INITIAL SCORE
    # -------------------------

    qualification_score = 0

    reasons = []

    # =========================
    # BUSINESS MATCHING
    # =========================

    if len(business_keywords) >= 2:

        qualification_score += 30

        reasons.append(
            "Strong business ICP match"
        )

    elif len(business_keywords) == 1:

        qualification_score += 15

        reasons.append(
            "Partial business ICP match"
        )

    # =========================
    # SCALING SIGNALS
    # =========================

    if len(scaling_signals) >= 1:

        qualification_score += 25

        reasons.append(
            "Scaling intent detected"
        )

    # =========================
    # PAIN SIGNALS
    # =========================

    if len(pain_keywords) >= 1:

        qualification_score += 20

        reasons.append(
            "Operational pain points detected"
        )

    # =========================
    # AUTOMATION SIGNALS
    # =========================

    if len(automation_keywords) >= 1:

        qualification_score += 15

        reasons.append(
            "Automation readiness detected"
        )

    # =========================
    # HIGH VALUE SIGNALS
    # =========================

    if len(high_value_signals) >= 1:

        qualification_score += 20

        reasons.append(
            "High-value company indicators"
        )

    # =========================
    # QUALIFICATION STATUS
    # =========================

    qualified = qualification_score >= 40

    # =========================
    # QUALIFICATION TIER
    # =========================

    if qualification_score >= 70:

        qualification_tier = "High Priority"

    elif qualification_score >= 50:

        qualification_tier = "Qualified"

    elif qualification_score >= 40:

        qualification_tier = "Potential"

    else:

        qualification_tier = "Low Priority"

    # =========================
    # FINAL RESULT
    # =========================

    # Cap score at 100

    qualification_score = min(
        qualification_score,
        100
    )

    result = {

        "qualified":
            qualified,

        "qualification_score":
            qualification_score,

        "qualification_tier":
            qualification_tier,

        "qualification_reasons":
            reasons
    }

    logger.info(
        f"Qualification score: "
        f"{qualification_score}"
    )

    logger.info(
        f"Qualification tier: "
        f"{qualification_tier}"
    )

    return result


# =========================
# TEST
# =========================

if __name__ == "__main__":

    sample_data = {

        "business_keywords": [
            "digital marketing agency",
            "saas startup"
        ],

        "scaling_signals": [
            "scaling fast"
        ],

        "pain_keywords": [
            "lead leakage"
        ],

        "automation_keywords": [
            "hubspot"
        ],

        "high_value_signals": [
            "venture-backed"
        ]
    }

    result = qualify_lead(
        sample_data
    )

    print("\nQUALIFICATION RESULT:\n")

    print(result)