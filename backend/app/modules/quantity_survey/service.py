"""Deterministic quantity calculations; no LLM is involved in this module."""

from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status

from app.modules.quantity_survey.schemas import (
    QuantitySurveyRequest,
    QuantitySurveyResponse,
    RoomQuantity,
    WallQuantity,
)

PRECISION = Decimal("0.001")


def _round(value: Decimal) -> Decimal:
    return value.quantize(PRECISION, rounding=ROUND_HALF_UP)


class QuantitySurveyService:
    def calculate(self, request: QuantitySurveyRequest) -> QuantitySurveyResponse:
        rooms = [
            RoomQuantity(name=room.name, area_m2=_round(room.length_m * room.width_m))
            for room in request.rooms
        ]
        walls: list[WallQuantity] = []

        for index, wall in enumerate(request.walls):
            gross_area = wall.length_m * wall.height_m
            opening_area = sum(
                (opening.width_m * opening.height_m for opening in wall.openings),
                start=Decimal("0"),
            )
            if opening_area > gross_area:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Openings exceed gross surface for wall {index + 1}",
                )
            net_area = gross_area - opening_area
            walls.append(
                WallQuantity(
                    gross_area_m2=_round(gross_area),
                    opening_area_m2=_round(opening_area),
                    net_area_m2=_round(net_area),
                    net_volume_m3=_round(net_area * wall.thickness_m),
                )
            )

        return QuantitySurveyResponse(
            rooms=rooms,
            walls=walls,
            total_floor_area_m2=_round(sum((room.area_m2 for room in rooms), Decimal("0"))),
            total_wall_net_area_m2=_round(sum((wall.net_area_m2 for wall in walls), Decimal("0"))),
            total_wall_net_volume_m3=_round(sum((wall.net_volume_m3 for wall in walls), Decimal("0"))),
        )
