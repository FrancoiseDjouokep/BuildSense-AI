from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.plan_analysis.gemini import GeminiPlanInterpreter
from app.modules.plan_analysis.models import AnalysisStatus, PlanAnalysis
from app.modules.plan_analysis.prompting import PLAN_EXTRACTION_PROMPT_VERSION
from app.modules.plan_analysis.schemas import PlanAnalysisResponse
from app.modules.upload.models import Plan, PlanStatus
from app.modules.upload.storage import PlanStorage


class PlanNotFoundError(Exception):
    """Raised when a plan does not exist in the requested project."""


class PlanAnalysisService:
    """Application service orchestrating architectural plan analysis."""

    def __init__(
        self,
        db: Session,
        storage: PlanStorage,
        interpreter: GeminiPlanInterpreter,
    ) -> None:
        self.db = db
        self.storage = storage
        self.interpreter = interpreter

    def analyse(
        self,
        project_id: UUID,
        plan_id: UUID,
    ) -> PlanAnalysisResponse:
        plan = self._get_plan(project_id, plan_id)
        plan.status = PlanStatus.PROCESSING
        analysis = PlanAnalysis(
            plan_id=plan.id,
            status=AnalysisStatus.PROCESSING,
            provider="gemini",
            model=self.interpreter.model,
            prompt_version=PLAN_EXTRACTION_PROMPT_VERSION,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        try:
            content = self.storage.get(plan.storage_key)

            extraction = self.interpreter.analyse(
                content=content,
                mime_type=plan.mime_type,
            )

            plan.status = PlanStatus.ANALYSED
            analysis.status = AnalysisStatus.COMPLETED
            analysis.result = extraction.model_dump(mode="json")
            analysis.completed_at = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(analysis)

            return PlanAnalysisResponse.model_validate(analysis)

        except Exception:
            self.db.rollback()

            plan = self._get_plan(project_id, plan_id)
            plan.status = PlanStatus.FAILED
            analysis = self.db.get(PlanAnalysis, analysis.id)
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "Plan analysis could not be completed."
            analysis.completed_at = datetime.now(UTC)
            self.db.commit()

            raise

    def list_analyses(
        self, project_id: UUID, plan_id: UUID
    ) -> list[PlanAnalysisResponse]:
        self._get_plan(project_id, plan_id)
        statement = (
            select(PlanAnalysis)
            .where(PlanAnalysis.plan_id == plan_id)
            .order_by(PlanAnalysis.created_at.desc())
        )
        return [
            PlanAnalysisResponse.model_validate(analysis)
            for analysis in self.db.scalars(statement).all()
        ]

    def get_analysis(
        self, project_id: UUID, plan_id: UUID, analysis_id: UUID
    ) -> PlanAnalysisResponse:
        self._get_plan(project_id, plan_id)
        statement = select(PlanAnalysis).where(
            PlanAnalysis.id == analysis_id,
            PlanAnalysis.plan_id == plan_id,
        )
        analysis = self.db.scalar(statement)
        if analysis is None:
            raise PlanNotFoundError("Plan analysis not found")
        return PlanAnalysisResponse.model_validate(analysis)

    def _get_plan(
        self,
        project_id: UUID,
        plan_id: UUID,
    ) -> Plan:
        statement = select(Plan).where(
            Plan.id == plan_id,
            Plan.project_id == project_id,
        )

        plan = self.db.scalar(statement)

        if plan is None:
            raise PlanNotFoundError("Plan not found")

        if plan.status == PlanStatus.ARCHIVED:
            raise ValueError("Archived plans cannot be analysed")

        return plan
