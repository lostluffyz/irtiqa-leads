from shared.logger import logger


# =========================
# HIGH SIGNAL KEYWORDS
# =========================

SIGNAL_KEYWORDS = [

    "seo",
    "marketing",
    "agency",
    "automation",
    "workflow",
    "growth",
    "scaling",
    "pipeline",
    "conversion",
    "crm",
    "lead",
    "paid media",
    "content",
    "campaign",
    "analytics",
    "ai",
    "operations",
    "performance",
    "revenue",
    "optimization"
]


# =========================
# SMART CONTEXT EXTRACTION
# =========================

def select_relevant_context(

    text,

    max_chunks=12
):

    logger.info(
        "Selecting relevant AI context"
    )

    paragraphs = text.split("\n")

    scored_chunks = []

    for chunk in paragraphs:

        chunk_lower = chunk.lower()

        score = 0

        for keyword in SIGNAL_KEYWORDS:

            if keyword in chunk_lower:

                score += 1

        if score > 0:

            scored_chunks.append(

                (
                    score,
                    chunk.strip()
                )
            )

    scored_chunks.sort(
        reverse=True
    )

    selected_chunks = [

        chunk
        for score, chunk
        in scored_chunks[:max_chunks]
    ]

    final_context = "\n".join(
        selected_chunks
    )

    logger.info(

        f"Selected "
        f"{len(selected_chunks)} "
        f"high-signal chunks"
    )

    return final_context