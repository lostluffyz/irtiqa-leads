def calculate_lead_score(enriched_lead):

    score = 0

    reasons = []

    # =========================
    # SIGNAL COUNTS
    # =========================

    business_count = len(

        enriched_lead.get(
            "business_keywords",
            []
        )
    )

    automation_count = len(

        enriched_lead.get(
            "automation_keywords",
            []
        )
    )

    scaling_count = len(

        enriched_lead.get(
            "scaling_signals",
            []
        )
    )

    pain_count = len(

        enriched_lead.get(
            "pain_points",
            []
        )
    )

    # =========================
    # BUSINESS SIGNAL DENSITY
    # =========================

    if business_count >= 10:

        score += 25

        reasons.append(
            "High business signal density"
        )

    elif business_count >= 5:

        score += 15

        reasons.append(
            "Strong business signal match"
        )

    # =========================
    # AUTOMATION SOPHISTICATION
    # =========================

    if automation_count >= 5:

        score += 20

        reasons.append(
            "Advanced automation maturity"
        )

    elif automation_count >= 2:

        score += 10

        reasons.append(
            "Automation readiness detected"
        )

    # =========================
    # SCALING SIGNALS
    # =========================

    if scaling_count >= 2:

        score += 20

        reasons.append(
            "Strong scaling indicators"
        )

    elif scaling_count >= 1:

        score += 10

        reasons.append(
            "Growth-stage signals detected"
        )

    # =========================
    # OPERATIONAL COMPLEXITY
    # =========================

    if pain_count >= 2:

        score += 15

        reasons.append(
            "Operational complexity detected"
        )

    elif pain_count >= 1:

        score += 8

        reasons.append(
            "Operational pain signals found"
        )

    # =========================
    # AUTHORITY SIGNALS
    # =========================

    website_text = enriched_lead.get(
        "text",
        ""
    ).lower()

    authority_keywords = [
        "fortune 500",
        "enterprise",
        "global",
        "billions revenue",
        "award-winning",
        "google premier partner",
        "trusted by",
        "500 companies",
        "millions",
        "countries"
    ]

    authority_matches = 0

    for keyword in authority_keywords:

        if keyword in website_text:

            authority_matches += 1

    if authority_matches >= 2:

        score += 20

        reasons.append(
            "Enterprise authority signals"
        )

    # =========================
    # INDUSTRY SCORING
    # =========================

    industry = enriched_lead.get(
        "industry_type",
        ""
    )

    if industry == "Digital Marketing Agency":

        score += 25

        reasons.append(
            "Strong industry match"
        )

    elif industry:

        score += 15

        reasons.append(
            "Partial industry match"
        )

    # =========================
    # EMAIL AVAILABILITY
    # =========================

    emails = enriched_lead.get(
        "emails",
        []
    )

    if emails:

        score += 10

        reasons.append(
            "Contact email found"
        )

    # =========================
    # WEBSITE QUALITY SIGNAL
    # =========================

    text_length = len(
        enriched_lead.get("text", "")
    )

    if business_count >= 8 and text_length > 2000:

        score += 10

        reasons.append(
            "Established website presence"
        )

    # =========================
    # SCORE NORMALIZATION
    # =========================

    if score > 100:

        score = 100

    # =========================
    # DETERMINE LEAD TIER
    # =========================

    if score >= 70:

        tier = "Hot Lead"

    elif score >= 40:

        tier = "Warm Lead"

    else:

        tier = "Cold Lead"

    reasons = list(set(reasons))

    return {
        "score": score,
        "tier": tier,
        "reasons": reasons
    }
