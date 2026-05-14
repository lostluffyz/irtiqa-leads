import json

from shared.ollama_client import ask_llm

from shared.json_utils import (
    safe_parse_json
)

# =========================
# PAIN POINT VALIDATION
# =========================

PAIN_POINT_VALIDATORS = {

    "CRM inefficiencies": [
        "crm",
        "salesforce",
        "hubspot",
        "pipeline",
        "lead tracking",
        "customer data",
        "conversion tracking",
        "tracking setup",
        "reporting",
        "analytics"
    ],

    "Manual workflows": [
        "manual",
        "workflow",
        "process",
        "operations",
        "coordination",
        "management",
        "checklist",
        "implementation",
        "optimization",
        "execution",
        "setup"
    ],

    "Scaling bottlenecks": [
        "scale",
        "growth",
        "headcount",
        "capacity",
        "expansion",
        "fast-growing"
    ],

    "Content production overload": [
        "content",
        "creative",
        "design",
        "graphics",
        "motion",
        "video",
        "audio",
        "writers",
        "production",
        "publishing",
        "campaigns",
        "assets",
        "branding",
        "media"
    ],

    "Marketing inefficiencies": [
        "marketing",
        "campaign",
        "ads",
        "seo",
        "conversion",
        "performance"
    ],

    "Sales pipeline problems": [
        "pipeline",
        "lead",
        "conversion",
        "sales",
        "prospect",
        "acquisition"
    ]
}


# =========================
# VALIDATE PAIN POINTS
# =========================

def validate_pain_points(
    pain_points
):

    validated = []

    for point in pain_points:

        # -------------------------
        # ENSURE DICT FORMAT
        # -------------------------

        if not isinstance(
            point,
            dict
        ):

            continue

        category = point.get(
            "category",
            ""
        ).strip()

        signal = point.get(
            "signal",
            ""
        ).strip().lower()

        # -------------------------
        # REQUIRE CATEGORY
        # -------------------------

        if not category:

            continue

        # -------------------------
        # TRUST VALID CATEGORY
        # -------------------------

        if category in PAIN_POINT_VALIDATORS:

            validated.append({

                "category": category,

                "signal": signal
            })

            continue

        # -------------------------
        # FALLBACK SIGNAL CHECK
        # -------------------------

        all_keywords = []

        for keywords in (
            PAIN_POINT_VALIDATORS.values()
        ):

            all_keywords.extend(
                keywords
            )

        if any(
            keyword in signal
            for keyword in all_keywords
        ):

            validated.append({

                "category": category,

                "signal": signal
            })

    return validated


# =========================
# EXTRACT PAIN POINTS
# =========================

def extract_pain_points(
    company_name,
    website_text
):

    prompt = f"""
You are an AI sales intelligence agent for Irtiqa AI.

Your task:
Analyze the website text and identify operational
signals, workflow complexity, scaling indicators,
or process challenges that are EXPLICITLY implied
by the text.

Do NOT invent problems.
Do NOT assume the company is failing.
Only identify signals supported by the website content.

Possible pain point categories:

- Lead generation problems
- Manual workflows
- Slow follow-up
- CRM inefficiencies
- Scaling bottlenecks
- Marketing inefficiencies
- Content production overload
- Poor automation
- Customer acquisition challenges
- Sales pipeline problems
- Team productivity issues
- Conversion optimization issues
- Multi-channel marketing complexity
- Reporting inefficiencies

Company Name:
{company_name}

Website Text:
{website_text}

Return ONLY valid JSON.

If no clear operational signals exist,
return an empty pain_points list.

Format:
{{
    "pain_points": [
        {{
            "category": "",
            "signal": ""
        }}
    ],
    "confidence": 0,
    "reasoning": ""
}}
"""

    response = ask_llm(
        prompt
    )

    print("\nRAW MODEL RESPONSE:\n")

    print(response)

    result = safe_parse_json(
        response
    )

    # =========================
    # PARSE FAILURE
    # =========================

    if not result:

        return {

            "pain_points": [],

            "confidence": 0,

            "reasoning":
                "Failed to parse model response"
        }

    # =========================
    # VALIDATE POINTS
    # =========================

    validated_points = validate_pain_points(

        result.get(
            "pain_points",
            []
        )
    )

    result["pain_points"] = (
        validated_points
    )

    return result


# =========================
# TESTING
# =========================

if __name__ == "__main__":

    sample_text = """
    We help SaaS companies scale through paid ads,
    SEO, AI marketing, content marketing,
    pipeline optimization, and automation.
    """

    result = extract_pain_points(

        "GrowthSpark Media",

        sample_text
    )

    print(result)