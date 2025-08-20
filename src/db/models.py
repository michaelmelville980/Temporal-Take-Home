from sqlalchemy import Column, Integer, String, DateTime, func, JSONB
from sqlalchemy.orm import declarative_base


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
    payment_id = Column()
    order_id = Column()
    status = Column()
    amount = Column()
    created_at = Column()

class Events(Base):
    __tablename__ = "events"
    id = Column()
    order_id = Column()
    type = Column()
    payload_json = Column()
    ts = Column()