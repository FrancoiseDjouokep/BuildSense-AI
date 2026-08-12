import uuid

from sqlalchemy import Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.core.database.base import Base  # ⚠️ ajuste selon ton Base déclaratif


class UnitPrice(Base):
    __tablename__ = "unit_prices"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    label = Column(String(255), nullable=False)
    unit = Column(String(10), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, server_default="XAF")