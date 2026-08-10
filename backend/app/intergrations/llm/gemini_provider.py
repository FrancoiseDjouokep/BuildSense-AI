import json

from google import genai

from app.core.config.settings import settings
from app.integrations.llm.base import LLMProvider
from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.prompting import build_plan_extraction_prompt


class GeminiProvider(LLMProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def extract_plan(self, file_bytes: bytes) -> PlanExtraction:

        prompt = build_plan_extraction_prompt()

        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                prompt,
                {
                    "mime_type": "application/pdf",
                    "data": file_bytes,
                },
            ],
        )

        data = json.loads(response.text)

        return PlanExtraction.model_validate(data)