from app.core.config.settings import settings
from app.integrations.llm.base import LLMProvider
from app.integrations.llm.gemini_provider import GeminiProvider


def get_llm_provider() -> LLMProvider:

    match settings.llm_provider.lower():

        case "gemini":
            return GeminiProvider()

        case _:
            raise ValueError(
                f"Unsupported provider: {settings.llm_provider}"
            )