from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.modules.quantity_survey.schemas import QuantitySurveyRequest, RoomInput, WallInput
from app.modules.quantity_survey.service import QuantitySurveyService


def test_calculates_room_and_wall_quantities() -> None:
    request = QuantitySurveyRequest(
        rooms=[RoomInput(name="Salon", length_m=Decimal("5.2"), width_m=Decimal("4.5"))],
        walls=[
            WallInput(
                length_m=Decimal("5"),
                height_m=Decimal("2.8"),
                thickness_m=Decimal("0.2"),
                openings=[{"width_m": "0.9", "height_m": "2.1"}],
            )
        ],
    )

    result = QuantitySurveyService().calculate(request)

    assert result.total_floor_area_m2 == Decimal("23.400")
    assert result.walls[0].gross_area_m2 == Decimal("14.000")
    assert result.walls[0].opening_area_m2 == Decimal("1.890")
    assert result.total_wall_net_area_m2 == Decimal("12.110")
    assert result.total_wall_net_volume_m3 == Decimal("2.422")


def test_rejects_openings_larger_than_wall() -> None:
    request = QuantitySurveyRequest(
        walls=[
            WallInput(
                length_m=Decimal("1"),
                height_m=Decimal("2"),
                thickness_m=Decimal("0.2"),
                openings=[{"width_m": "2", "height_m": "2"}],
            )
        ]
    )

    with pytest.raises(HTTPException, match="Openings exceed"):
        QuantitySurveyService().calculate(request)
