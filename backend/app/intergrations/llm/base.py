from abc import ABC, abstractmethod

from app.modules.plan_analysis.contracts import PlanExtraction


class LLMProvider(ABC):
    """Base class for every LLM provider."""

    @abstractmethod
    async def extract_plan(self, file_bytes: bytes) -> PlanExtraction:
        """Extract structured observations from a plan."""
        raise NotImplementedError