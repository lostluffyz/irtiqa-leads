import json
import re


# =========================
# SAFE JSON PARSER
# =========================

def safe_parse_json(raw_text):

    if not raw_text:

        return None

    # =========================
    # REMOVE MARKDOWN WRAPPERS
    # =========================

    cleaned = raw_text.strip()

    cleaned = cleaned.replace(
        "```json",
        ""
    )

    cleaned = cleaned.replace(
        "```",
        ""
    )

    # =========================
    # REMOVE CONTROL CHARACTERS
    # =========================

    cleaned = re.sub(

        r"[\x00-\x1F\x7F]",

        "",

        cleaned
    )

    # =========================
    # EXTRACT JSON OBJECT
    # =========================

    json_match = re.search(

        r"\{.*\}",

        cleaned,

        re.DOTALL
    )

    if json_match:

        cleaned = json_match.group(0)

    # =========================
    # REMOVE TRAILING COMMAS
    # =========================

    cleaned = re.sub(

        r",\s*}",

        "}",

        cleaned
    )

    cleaned = re.sub(

        r",\s*]",

        "]",

        cleaned
    )

    # =========================
    # ATTEMPT JSON PARSE
    # =========================

    try:

        return json.loads(cleaned)

    except Exception as e:

        print("\nJSON PARSE ERROR:\n")

        print(e)

        return None