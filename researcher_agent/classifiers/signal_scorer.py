# =========================
# SIGNAL WEIGHTS
# =========================

SIGNAL_WEIGHTS = {

    "automation": 15,

    "analytics": 10,

    "tracking": 10,

    "conversion": 15,

    "scaling": 20,

    "growth": 15,

    "performance marketing": 10,

    "multi-channel": 15,

    "crm": 15,

    "enterprise": 20,

    "workflow": 10,

    "optimization": 10,

    "reporting": 10,

    "roi": 10,

    "paid ads": 10,

    "seo": 10,

    "email marketing": 10
}


# =========================
# DETECT SIGNALS
# =========================

def score_signals(website_text):

    text = website_text.lower()

    signal_score = 0

    detected_signals = []

    for signal, weight in SIGNAL_WEIGHTS.items():

        if signal in text:

            signal_score += weight

            detected_signals.append(signal)

    # =========================
    # NORMALIZE SCORE
    # =========================

    if signal_score > 100:

        signal_score = 100

    # =========================
    # DETERMINE INTENT LEVEL
    # =========================

    if signal_score >= 70:

        intent_level = "High Intent"

    elif signal_score >= 40:

        intent_level = "Medium Intent"

    else:

        intent_level = "Low Intent"

    return {

        "signal_score": signal_score,

        "intent_level": intent_level,

        "detected_signals": detected_signals
    }


# =========================
# TESTING
# =========================

if __name__ == "__main__":

    sample_text = """
    We help enterprises scale using automation,
    CRM optimization, analytics dashboards,
    SEO, paid ads, and workflow automation.
    """

    result = score_signals(sample_text)

    print(result)