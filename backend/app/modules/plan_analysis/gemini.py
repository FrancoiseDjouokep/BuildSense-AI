import json

from google import genai
from google.genai import types

from app.core.config.settings import settings
from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.prompting import build_plan_extraction_prompt


GEMINI_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "building": {
            "type": "object",
            "properties": {
                "scale": {
                    "type": "string",
                    "description": "Plan scale, for example 1:100",
                },
                "floors": {
                    "type": "integer",
                    "description": "Number of floors",
                },
            },
            "required": ["scale", "floors"],
        },
        "rooms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "length_m": {
                        "type": "number",
                    },
                    "width_m": {
                        "type": "number",
                    },
                    "level": {
                        "type": "integer",
                    },
                },
                "required": [
                    "name",
                    "length_m",
                    "width_m",
                    "level",
                ],
            },
        },
        "walls": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "length_m": {
                        "type": "number",
                    },
                    "height_m": {
                        "type": "number",
                    },
                    "thickness_m": {
                        "type": "number",
                    },
                    "openings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "kind": {
                                    "type": "string",
                                },
                                "width_m": {
                                    "type": "number",
                                },
                                "height_m": {
                                    "type": "number",
                                },
                            },
                            "required": [
                                "kind",
                                "width_m",
                                "height_m",
                            ],
                        },
                    },
                },
                "required": [
                    "length_m",
                    "height_m",
                    "thickness_m",
                    "openings",
                ],
            },
        },
        "confidence": {
            "type": "number",
        },
        "source_provider": {
            "type": "string",
        },
        "source_model": {
            "type": "string",
        },
    },
    "required": [
        "building",
        "rooms",
        "walls",
        "confidence",
        "source_provider",
        "source_model",
    ],
}


class GeminiPlanInterpreter:
    """Gemini adapter responsible only for interpreting architectural plans."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def analyse(
        self,
        content: bytes,
        mime_type: str,
    ) -> PlanExtraction:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(
                    data=content,
                    mime_type=mime_type,
                ),
                build_plan_extraction_prompt(),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GEMINI_RESPONSE_SCHEMA,
                temperature=0,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Gemini returned invalid JSON."
            ) from error

        return PlanExtraction.model_validate(payload)