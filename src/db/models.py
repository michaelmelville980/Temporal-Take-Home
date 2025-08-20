from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Orders(Base):
    __tablename__ = "orders"
    id = Column() #Added via order_received function (order_id)
    state = Column() #received, validated,
    address_json = Column()
    created_at = Column()
    updated_at = Column()

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