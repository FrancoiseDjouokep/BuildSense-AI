from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.session import get_db  # ⚠️ ajuste si nécessaire
from app.modules.pricing.models import UnitPrice
from app.modules.pricing.schemas import PricingRequest, PricingResponse, UnitPriceData
from app.modules.pricing.service import PricingService
from app.modules.quantity_survey.router import get_quantity_survey_for_plan

router = APIRouter(prefix="/pricing", tags=["Pricing"])


def _build_catalog(db: Session, codes: set[str]) -> dict[str, UnitPriceData]:
    rows = db.query(UnitPrice).filter(UnitPrice.code.in_(codes)).all()
    return {
        row.code: UnitPriceData(code=row.code, label=row.label, unit=row.unit, unit_price=row.unit_price)
        for row in rows
    }


@router.post("/calculate", response_model=PricingResponse)
def calculate_pricing(request: PricingRequest, db: Session = Depends(get_db)) -> PricingResponse:
    codes = {item.code for item in request.items}
    catalog = _build_catalog(db, codes)
    return PricingService().price_items(request.items, catalog)


@router.get("/by-plan/{plan_id}", response_model=PricingResponse)
def get_devis_for_plan(plan_id: UUID, db: Session = Depends(get_db)) -> PricingResponse:
    """Le devis complet et chiffré pour un plan, en un seul appel."""
    survey = get_quantity_survey_for_plan(plan_id, db)
    codes = {item.code for item in survey.items}
    catalog = _build_catalog(db, codes)
    return PricingService().price_items(survey.items, catalog)