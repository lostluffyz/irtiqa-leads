from shared.ollama_client import ask_llm


def generate_linkedin_message(enriched_lead):

    company_name = enriched_lead.get(
        "title",
        "your company"
    )

    industry = enriched_lead.get(
        "industry_type",
        "business"
    )

    tier = enriched_lead.get(
        "tier",
        "Lead"
    )

    pain_points = enriched_lead.get(
        "pain_points",
        []
    )

    pain_point_text = ""

    # =========================
    # BUILD PAIN POINT TEXT
    # =========================

    for pain in pain_points:

        # -------------------------
        # DICT FORMAT
        # -------------------------

        if isinstance(pain, dict):

            category = pain.get(
                "category",
                ""
            )

            if category:

                pain_point_text += (
                    f"- {category}\n"
                )

        # -------------------------
        # STRING FORMAT
        # -------------------------

        elif isinstance(pain, str):

            pain_point_text += (
                f"- {pain}\n"
            )

    # =========================
    # PROMPT
    # =========================

    prompt = f"""
You are an AI SDR for Irtiqa AI.

Your job:
Write short founder-style LinkedIn outreach messages.

The message should:
- feel human
- feel observational
- sound curious
- avoid corporate language
- avoid sounding salesy
- avoid sounding like ChatGPT
- avoid "would love to connect"
- avoid buzzwords
- avoid fake enthusiasm
- avoid pretending to know the company deeply
- never diagnose aggressively
- never oversell
- keep under 3 sentences

GOOD EXAMPLES:

Example 1:
Saw your team leaning hard into AI-native search lately.
Feels like agencies are getting pulled into content volume chaos right now.
Curious how you're handling that internally.

Example 2:
Noticed you’re scaling paid media pretty aggressively.
Feels like keeping campaign quality consistent gets messy fast at that stage.
Wondering how your team’s approaching that balance.

Example 3:
Looks like your team has been pushing hard on SEO + content velocity.
Feels like most agencies are trying to figure out how AI changes workflows right now.
Curious what’s actually been working for you.

Company:
{company_name}

Industry:
{industry}

Lead Tier:
{tier}

Pain Points:
{pain_point_text}

Return ONLY the message text.
"""

    response = ask_llm(prompt)

    return response.strip()


# =========================
# TEST
# =========================

if __name__ == "__main__":

    sample_lead = {

        "title": "Single Grain",

        "industry_type":
            "Digital Marketing Agency",

        "tier":
            "Warm Lead",

        "pain_points": [

            {
                "category":
                    "Scaling bottlenecks"
            },

            {
                "category":
                    "Manual workflows"
            },

            "Lead generation overload"
        ]
    }

    result = generate_linkedin_message(
        sample_lead
    )

    print("\nLINKEDIN MESSAGE:\n")

    print(result)