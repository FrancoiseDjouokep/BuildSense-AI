from decimal import Decimal
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field

PositiveDecimal = Annotated[Decimal, Field(gt=0)]
NonNegativeDecimal = Annotated[Decimal, Field(ge=0)]

DEFAULT_CEILING_HEIGHT_M = Decimal("2.50")


class QuantityUnit(str, Enum):
    M2 = "m2"
    M3 = "m3"
    ML = "ml"
    UNITE = "unite"


class OpeningInput(BaseModel):
    kind: str = Field(pattern=r"^(door|window)$")
    width_m: PositiveDecimal
    height_m: PositiveDecimal


class RoomInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    length_m: PositiveDecimal
    width_m: PositiveDecimal
    height_m: PositiveDecimal = DEFAULT_CEILING_HEIGHT_M


class WallInput(BaseModel):
    length_m: PositiveDecimal
    height_m: PositiveDecimal
    thickness_m: PositiveDecimal
    openings: list[OpeningInput] = Field(default_factory=list)


class StairInput(BaseModel):
    width_m: PositiveDecimal
    total_height_m: PositiveDecimal
    thickness_m: PositiveDecimal = Decimal("0.15")


class QuantitySurveyRequest(BaseModel):
    rooms: list[RoomInput] = Field(default_factory=list)
    walls: list[WallInput] = Field(default_factory=list)
    stairs: list[StairInput] = Field(default_factory=list)


class RoomQuantity(BaseModel):
    name: str
    area_m2: NonNegativeDecimal
    perimeter_m: NonNegativeDecimal
    wall_paint_area_m2: NonNegativeDecimal
    skirting_length_m: NonNegativeDecimal


class WallQuantity(BaseModel):
    gross_area_m2: NonNegativeDecimal
    opening_area_m2: NonNegativeDecimal
    net_area_m2: NonNegativeDecimal
    net_volume_m3: NonNegativeDecimal
    door_count: int
    door_area_m2: NonNegativeDecimal
    window_count: int
    window_area_m2: NonNegativeDecimal


class StairQuantity(BaseModel):
    concrete_volume_m3: NonNegativeDecimal


class BillOfQuantityItem(BaseModel):
    """Une ligne de métré, prête à être chiffrée par le Service Pricing."""

    code: str
    label: str
    quantity: NonNegativeDecimal
    unit: QuantityUnit
    room_name: str | None = None


class QuantitySurveyResponse(BaseModel):
    rooms: list[RoomQuantity]
    walls: list[WallQuantity]
    stairs: list[StairQuantity]
    total_floor_area_m2: NonNegativeDecimal
    total_wall_net_area_m2: NonNegativeDecimal
    total_wall_net_volume_m3: NonNegativeDecimal
    total_stair_concrete_volume_m3: NonNegativeDecimal
    total_door_count: int
    total_window_count: int
    items: list[BillOfQuantityItem]