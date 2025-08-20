from sqlalchemy import Column, Integer, String, DateTime, func, JSONB, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
metadata = Base.metadata

class Orders(Base):
    __tablename__ = "orders"
    id = Column(String(64), primary_key=True)
    state = Column(String(30), nullable=False, server_default="received") 
    address_json = Column(JSONB, nullable=True)
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
    id = Column()
    order_id = Column()
    type = Column()
    payload_json = Column()
    ts = Column()