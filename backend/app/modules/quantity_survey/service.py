"""Deterministic quantity calculations; no LLM is involved in this module."""

from decimal import ROUND_HALF_UP, Decimal

from fastapi import HTTPException, status

from app.modules.plan_analysis.contracts import PlanExtraction
from app.modules.quantity_survey.schemas import (
    BillOfQuantityItem,
    OpeningInput,
    QuantitySurveyRequest,
    QuantitySurveyResponse,
    QuantityUnit,
    RoomInput,
    RoomQuantity,
    StairInput,
    StairQuantity,
    WallInput,
    WallQuantity,
)

PRECISION = Decimal("0.001")
STAIR_PITCH_RATIO = Decimal("1.54")  # pente standard ~33°, approximation MVP
STAIR_STEP_FACTOR = Decimal("1.3")  # majoration forfaitaire marches vs paillasse nue


def _round(value: Decimal) -> Decimal:
    return value.quantize(PRECISION, rounding=ROUND_HALF_UP)


class QuantitySurveyService:
    def calculate(self, request: QuantitySurveyRequest) -> QuantitySurveyResponse:
        rooms: list[RoomQuantity] = []
        items: list[BillOfQuantityItem] = []

        for room in request.rooms:
            area = room.length_m * room.width_m
            perimeter = 2 * (room.length_m + room.width_m)
            wall_paint_area = perimeter * room.height_m
            skirting_length = perimeter

            rooms.append(
                RoomQuantity(
                    name=room.name,
                    area_m2=_round(area),
                    perimeter_m=_round(perimeter),
                    wall_paint_area_m2=_round(wall_paint_area),
                    skirting_length_m=_round(skirting_length),
                )
            )

            items.append(BillOfQuantityItem(
                code="SOL-REVET", label=f"Revêtement de sol - {room.name}",
                quantity=_round(area), unit=QuantityUnit.M2, room_name=room.name,
            ))
            items.append(BillOfQuantityItem(
                code="MUR-PEINTURE", label=f"Peinture murs (brut) - {room.name}",
                quantity=_round(wall_paint_area), unit=QuantityUnit.M2, room_name=room.name,
            ))
            items.append(BillOfQuantityItem(
                code="SOL-PLINTHE", label=f"Plinthes (brut) - {room.name}",
                quantity=_round(skirting_length), unit=QuantityUnit.ML, room_name=room.name,
            ))

        walls: list[WallQuantity] = []
        total_door_count = 0
        total_window_count = 0

        for index, wall in enumerate(request.walls):
            gross_area = wall.length_m * wall.height_m
            opening_area = sum((o.width_m * o.height_m for o in wall.openings), start=Decimal(0))

            if opening_area > gross_area:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Openings exceed gross surface for wall {index + 1}",
                )

            net_area = gross_area - opening_area
            doors = [o for o in wall.openings if o.kind == "door"]
            windows = [o for o in wall.openings if o.kind == "window"]
            door_area = sum((d.width_m * d.height_m for d in doors), Decimal(0))
            window_area = sum((w.width_m * w.height_m for w in windows), Decimal(0))
            total_door_count += len(doors)
            total_window_count += len(windows)

            walls.append(WallQuantity(
                gross_area_m2=_round(gross_area),
                opening_area_m2=_round(opening_area),
                net_area_m2=_round(net_area),
                net_volume_m3=_round(net_area * wall.thickness_m),
                door_count=len(doors),
                door_area_m2=_round(door_area),
                window_count=len(windows),
                window_area_m2=_round(window_area),
            ))

            items.append(BillOfQuantityItem(
                code="MUR-MACON", label=f"Maçonnerie mur {index + 1}",
                quantity=_round(net_area * wall.thickness_m), unit=QuantityUnit.M3,
            ))
            if doors:
                items.append(BillOfQuantityItem(
                    code="MENUIS-PORTE", label=f"Pose de porte(s) - mur {index + 1}",
                    quantity=Decimal(len(doors)), unit=QuantityUnit.UNITE,
                ))
            if windows:
                items.append(BillOfQuantityItem(
                    code="MENUIS-FENETRE", label=f"Pose de fenêtre(s) - mur {index + 1}",
                    quantity=Decimal(len(windows)), unit=QuantityUnit.UNITE,
                ))

        stairs: list[StairQuantity] = []
        for index, stair in enumerate(request.stairs):
            horizontal_run = stair.total_height_m * STAIR_PITCH_RATIO
            slab_volume = stair.width_m * horizontal_run * stair.thickness_m
            concrete_volume = _round(slab_volume * STAIR_STEP_FACTOR)

            stairs.append(StairQuantity(concrete_volume_m3=concrete_volume))
            items.append(BillOfQuantityItem(
                code="STRUCT-ESCALIER", label=f"Escalier béton {index + 1} (approximation)",
                quantity=concrete_volume, unit=QuantityUnit.M3,
            ))

        return QuantitySurveyResponse(
            rooms=rooms,
            walls=walls,
            stairs=stairs,
            total_floor_area_m2=_round(sum((r.area_m2 for r in rooms), Decimal(0))),
            total_wall_net_area_m2=_round(sum((w.net_area_m2 for w in walls), Decimal(0))),
            total_wall_net_volume_m3=_round(sum((w.net_volume_m3 for w in walls), Decimal(0))),
            total_stair_concrete_volume_m3=_round(sum((s.concrete_volume_m3 for s in stairs), Decimal(0))),
            total_door_count=total_door_count,
            total_window_count=total_window_count,
            items=items,
        )

    def calculate_from_extraction(self, extraction: PlanExtraction) -> QuantitySurveyResponse:
        default_height = extraction.building.default_ceiling_height_m

        request = QuantitySurveyRequest(
            rooms=[
                RoomInput(
                    name=room.name, length_m=room.length_m, width_m=room.width_m,
                    height_m=room.height_m or default_height,
                )
                for room in extraction.rooms
            ],
            walls=[
                WallInput(
                    length_m=wall.length_m, height_m=wall.height_m, thickness_m=wall.thickness_m,
                    openings=[
                        OpeningInput(kind=o.kind, width_m=o.width_m, height_m=o.height_m)
                        for o in wall.openings
                    ],
                )
                for wall in extraction.walls
            ],
            stairs=[
                StairInput(
                    width_m=stair.width_m,
                    total_height_m=stair.total_height_m,
                    thickness_m=stair.thickness_m,
                )
                for stair in extraction.stairs
            ],
        )

        return self.calculate(request)