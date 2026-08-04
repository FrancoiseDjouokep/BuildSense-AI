from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

PositiveDecimal = Annotated[Decimal, Field(gt=0)]
NonNegativeDecimal = Annotated[Decimal, Field(ge=0)]


class OpeningInput(BaseModel):
    width_m: PositiveDecimal
    height_m: PositiveDecimal


class RoomInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    length_m: PositiveDecimal
    width_m: PositiveDecimal


class WallInput(BaseModel):
    length_m: PositiveDecimal
    height_m: PositiveDecimal
    thickness_m: PositiveDecimal
    openings: list[OpeningInput] = Field(default_factory=list)


class QuantitySurveyRequest(BaseModel):
    rooms: list[RoomInput] = Field(default_factory=list)
    walls: list[WallInput] = Field(default_factory=list)


class RoomQuantity(BaseModel):
    name: str
    area_m2: NonNegativeDecimal


class WallQuantity(BaseModel):
    gross_area_m2: NonNegativeDecimal
    opening_area_m2: NonNegativeDecimal
    net_area_m2: NonNegativeDecimal
    net_volume_m3: NonNegativeDecimal


class QuantitySurveyResponse(BaseModel):
    rooms: list[RoomQuantity]
    walls: list[WallQuantity]
    total_floor_area_m2: NonNegativeDecimal
    total_wall_net_area_m2: NonNegativeDecimal
    total_wall_net_volume_m3: NonNegativeDecimal
