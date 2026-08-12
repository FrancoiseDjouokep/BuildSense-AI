# tests/test_pricing.py — nouveau fichier
from decimal import Decimal

from app.modules.pricing.schemas import UnitPriceData
from app.modules.pricing.service import PricingService
from app.modules.quantity_survey.schemas import BillOfQuantityItem, QuantityUnit


def test_prices_known_items_and_flags_unpriced() -> None:
    items = [
        BillOfQuantityItem(code="SOL-REVET", label="Revêtement - Salon",
                            quantity=Decimal("23.4"), unit=QuantityUnit.M2, room_name="Salon"),
        BillOfQuantityItem(code="INCONNU", label="???", quantity=Decimal("1"), unit=QuantityUnit.UNITE),
    ]
    catalog = {
        "SOL-REVET": UnitPriceData(code="SOL-REVET", label="Revêtement de sol", unit="m2", unit_price=Decimal("8000")),
    }

    result = PricingService().price_items(items, catalog)

    assert result.subtotal == Decimal("187200.00")
    assert result.unpriced_codes == ["INCONNU"]