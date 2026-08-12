"""Deterministic pricing calculations; the unit-price catalog is injected, not queried here."""

from decimal import ROUND_HALF_UP, Decimal

from app.modules.pricing.schemas import PricingLineItem, PricingResponse, UnitPriceData
from app.modules.quantity_survey.schemas import BillOfQuantityItem

PRECISION = Decimal("0.01")


def _round(value: Decimal) -> Decimal:
    return value.quantize(PRECISION, rounding=ROUND_HALF_UP)


class PricingService:
    def price_items(
        self,
        items: list[BillOfQuantityItem],
        catalog: dict[str, UnitPriceData],
    ) -> PricingResponse:
        lines: list[PricingLineItem] = []
        unpriced: list[str] = []

        for item in items:
            unit_price = catalog.get(item.code)
            if unit_price is None:
                unpriced.append(item.code)
                continue

            amount = _round(item.quantity * unit_price.unit_price)
            lines.append(PricingLineItem(
                code=item.code, label=item.label, quantity=item.quantity,
                unit=item.unit.value, unit_price=unit_price.unit_price,
                amount=amount, room_name=item.room_name,
            ))

        subtotal = _round(sum((line.amount for line in lines), Decimal(0)))

        return PricingResponse(
            lines=lines,
            unpriced_codes=sorted(set(unpriced)),
            subtotal=subtotal,
        )