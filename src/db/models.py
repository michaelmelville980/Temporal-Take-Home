from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import JSON
from .database import Base

metadata = Base.metadata

class Orders(Base):
    __tablename__ = "orders"
    id = Column(String(64), primary_key=True)
    items = Column(JSON, nullable=True)
    state = Column(String(30), nullable=False, server_default="received") 
    address_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Payments(Base):
    __tablename__ = "payments"
    payment_id = Column(String(64), primary_key=True)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Events(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(64), nullable=False)
    payload_json = Column(JSON, nullable=True)
    ts = Column(DateTime(timezone=True), nullable=False, server_default=func.now())