from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.plan_analysis.gemini import GeminiPlanInterpreter
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
    ) -> PlanExtraction:
        plan = self._get_plan(project_id, plan_id)

        plan.status = PlanStatus.PROCESSING
        self.db.commit()

        try:
            content = self.storage.get(plan.storage_key)

            extraction = self.interpreter.analyse(
                content=content,
                mime_type=plan.mime_type,
            )

            plan.status = PlanStatus.ANALYSED
            self.db.commit()

            return extraction

        except Exception:
            self.db.rollback()

            plan = self._get_plan(project_id, plan_id)
            plan.status = PlanStatus.FAILED
            self.db.commit()

            raise

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