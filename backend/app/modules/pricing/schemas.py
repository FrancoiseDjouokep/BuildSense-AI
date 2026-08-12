from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from app.modules.quantity_survey.schemas import BillOfQuantityItem

NonNegativeDecimal = Annotated[Decimal, Field(ge=0)]


class UnitPriceData(BaseModel):
    code: str
    label: str
    unit: str
    unit_price: NonNegativeDecimal


class PricingLineItem(BaseModel):
    code: str
    label: str
    quantity: NonNegativeDecimal
    unit: str
    unit_price: NonNegativeDecimal
    amount: NonNegativeDecimal
    room_name: str | None = None


class PricingRequest(BaseModel):
    items: list[BillOfQuantityItem]


class PricingResponse(BaseModel):
    lines: list[PricingLineItem]
    unpriced_codes: list[str]
    subtotal: NonNegativeDecimal
    currency: str = "XAF"