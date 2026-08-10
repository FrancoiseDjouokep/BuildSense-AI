"""Validated, provider-neutral contract for an interpreted architectural plan."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

PositiveDecimal = Annotated[Decimal, Field(gt=0)]


class BuildingObservation(BaseModel):
    scale: str = Field(pattern=r"^1:\d+$")
    floors: int = Field(ge=1, le=200)


class RoomObservation(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    length_m: PositiveDecimal
    width_m: PositiveDecimal
    level: int = Field(default=0, ge=0)


class OpeningObservation(BaseModel):
    kind: str = Field(pattern=r"^(door|window)$")
    width_m: PositiveDecimal
    height_m: PositiveDecimal


class WallObservation(BaseModel):
    length_m: PositiveDecimal
    height_m: PositiveDecimal
    thickness_m: PositiveDecimal
    openings: list[OpeningObservation] = Field(default_factory=list)


class PlanExtraction(BaseModel):
    """Strict JSON payload accepted from a vision provider after normalisation."""

    model_config = ConfigDict(extra="forbid")

    building: BuildingObservation
    rooms: list[RoomObservation] = Field(default_factory=list)
    walls: list[WallObservation] = Field(default_factory=list)
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
    source_provider: str = Field(min_length=1, max_length=50)
    source_model: str = Field(min_length=1, max_length=100)

    @field_validator("rooms", "walls")
    @classmethod
    def limit_collection_size(cls, items: list[object]) -> list[object]:
        if len(items) > 10_000:
            raise ValueError("A plan cannot contain more than 10,000 elements")
        return items