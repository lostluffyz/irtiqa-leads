import requests

from shared.config import (
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT
)

from shared.logger import (
    logger
)


# =========================
# ASK LOCAL LLM
# =========================

def ask_llm(

    prompt: str,

    model: str = OLLAMA_MODEL

) -> str:

    logger.info(
        f"Sending prompt to "
        f"{model}"
    )

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": model,

                "prompt": prompt,

                "stream": False
            },

            timeout=OLLAMA_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        )

    except Exception as e:

        logger.error(
            f"Ollama request failed: {e}"
        )

        return ""