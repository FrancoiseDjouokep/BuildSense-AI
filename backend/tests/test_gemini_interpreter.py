import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.modules.plan_analysis.gemini import GeminiPlanInterpreter


def test_overrides_provider_metadata_returned_by_model() -> None:
    interpreter = object.__new__(GeminiPlanInterpreter)
    interpreter.client = MagicMock()
    interpreter.model = "gemini-test-model"
    interpreter.client.models.generate_content.return_value = SimpleNamespace(
        text=json.dumps(
            {
                "building": {"scale": "1:100", "floors": 1},
                "rooms": [],
                "walls": [],
                "confidence": 0.9,
                "source_provider": "untrusted-value",
                "source_model": "untrusted-value",
            }
        )
    )

    extraction = interpreter.analyse(b"%PDF-1.7", "application/pdf")

    assert extraction.source_provider == "gemini"
    assert extraction.source_model == "gemini-test-model"
