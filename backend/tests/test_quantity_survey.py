from decimal import Decimal

import pytest
from fastapi import HTTPException

from app.modules.quantity_survey.schemas import (
    QuantitySurveyRequest,
    RoomInput,
    StairInput,
    WallInput,
)
from app.modules.quantity_survey.service import QuantitySurveyService


def test_calculates_room_and_wall_quantities() -> None:
    request = QuantitySurveyRequest(
        rooms=[
            RoomInput(
                name="Salon",
                length_m=Decimal("5.2"),
                width_m=Decimal("4.5"),
                height_m=Decimal("2.5"),
            )
        ],
        walls=[
            WallInput(
                length_m=Decimal("5"),
                height_m=Decimal("2.8"),
                thickness_m=Decimal("0.2"),
                openings=[{"kind": "door", "width_m": "0.9", "height_m": "2.1"}],
            )
        ],
    )

    result = QuantitySurveyService().calculate(request)

    assert result.total_floor_area_m2 == Decimal("23.400")
    assert result.rooms[0].perimeter_m == Decimal("19.400")
    assert result.rooms[0].wall_paint_area_m2 == Decimal("48.500")
    assert result.walls[0].gross_area_m2 == Decimal("14.000")
    assert result.walls[0].opening_area_m2 == Decimal("1.890")
    assert result.walls[0].door_count == 1
    assert result.walls[0].window_count == 0
    assert result.total_door_count == 1
    assert result.total_window_count == 0
    assert result.total_wall_net_area_m2 == Decimal("12.110")
    assert result.total_wall_net_volume_m3 == Decimal("2.422")


def test_generates_bill_of_quantity_items() -> None:
    request = QuantitySurveyRequest(
        rooms=[RoomInput(name="Salon", length_m=Decimal("5"), width_m=Decimal("4"))],
        walls=[],
    )

    result = QuantitySurveyService().calculate(request)
    codes = {item.code for item in result.items}

    assert codes == {"SOL-REVET", "MUR-PEINTURE", "SOL-PLINTHE"}


def test_room_uses_default_ceiling_height_when_not_specified() -> None:
    request = QuantitySurveyRequest(
        rooms=[RoomInput(name="Chambre", length_m=Decimal("3"), width_m=Decimal("3"))],
    )

    result = QuantitySurveyService().calculate(request)

    assert result.rooms[0].wall_paint_area_m2 == Decimal("30.000")


def test_rejects_openings_larger_than_wall() -> None:
    request = QuantitySurveyRequest(
        walls=[
            WallInput(
                length_m=Decimal("1"),
                height_m=Decimal("2"),
                thickness_m=Decimal("0.2"),
                openings=[{"kind": "window", "width_m": "2", "height_m": "2"}],
            )
        ]
    )

    with pytest.raises(HTTPException, match="Openings exceed"):
        QuantitySurveyService().calculate(request)


def test_calculates_stair_concrete_volume() -> None:
    request = QuantitySurveyRequest(
        stairs=[StairInput(width_m=Decimal("1"), total_height_m=Decimal("2.8"))]
    )
    result = QuantitySurveyService().calculate(request)

    assert result.stairs[0].concrete_volume_m3 > Decimal("0")
    assert any(item.code == "STRUCT-ESCALIER" for item in result.items)