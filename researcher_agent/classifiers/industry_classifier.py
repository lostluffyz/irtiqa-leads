
from shared.logger import logger
from shared.json_utils import (
    safe_parse_json
)
from shared.ollama_client import ask_llm

from researcher_agent.classifiers.keyword_matcher import (
    match_keywords
)

def classify_industry(
    company_name,
    description,
    keyword_result,
    website_text=""
):
    
    # =========================
    # KEYWORD MATCHING
    # =========================

    business_keywords = keyword_result.get(
        "business_keywords",
        []
    )

    # =========================
    # HYBRID INDUSTRY DETECTION
    # =========================

    keyword_industry_map = {

        "marketing agency":
            "Digital Marketing Agency",

        "digital marketing agency":
            "Digital Marketing Agency",

        "performance marketing agency":
            "Digital Marketing Agency",

        "lead generation agency":
            "Lead Generation Agency",

        "real estate brokerage":
            "Real Estate",

        "property management":
            "Real Estate",

        "law firm":
            "Legal Services",

        "dental clinic":
            "Healthcare",

        "medical clinic":
            "Healthcare",

        "software development":
            "Software Development",

        "saas startup":
            "SaaS",

        "it services":
            "IT Services",

        "recruitment agency":
            "Recruitment Agency",

        "consulting firm":
            "Consulting"
    }

    detected_industries = []

    for keyword in business_keywords:

        if keyword in keyword_industry_map:

            detected_industries.append(

                keyword_industry_map[
                    keyword
                ]
            )

    # -------------------------
    # KEYWORD CONFIDENCE
    # -------------------------

    if len(detected_industries) >= 1:

        most_common = max(
            set(detected_industries),
            key=detected_industries.count
        )

        logger.info(
            f"Keyword industry match: "
            f"{most_common}"
        )

        return {

            "industry_type":
                most_common,

            "industry_tier":
                "Tier 1",

            "confidence":
                90,

            "reasoning":
                "Detected through "
                "keyword intelligence"
        }

    prompt = f"""
You are an industry classification AI for Irtiqa AI.

Your task:
Classify the company into one of these categories.

Tier 1:
- Digital Marketing Agency
- Lead Generation Agency
- Real Estate
- Insurance Brokerage
- Solar/HVAC/Home Services
- Dental/Medical Clinic
- Law Firm
- IT Services/MSP
- Recruitment Agency
- B2B Consulting
- SaaS Startup
- Call Center

Tier 2:
- Accounting Firm
- Coaching Business
- Business Consultancy
- Virtual Assistant Agency
- BPO Company

Emerging Niches:
- AI Wellness
- FinTech
- AgriTech
- GreenTech
- Creator Platform
- HealthTech
- Community Platform

If there is no clear match:
Return "No Match"

Company Name:
{company_name}

Description:
{description}

Website Text:
{website_text}

Return ONLY valid JSON.

Format:
{{
    "industry_tier": "",
    "industry_type": "",
    "confidence": 0,
    "reasoning": ""
}}
"""

    response = ask_llm(prompt)

    result = safe_parse_json(response)

    if result:
        return result

    return {
        "industry_tier": "Unknown",
        "industry_type": "Unknown",
        "confidence": 0,
        "reasoning": "Failed to parse model response"
    }
