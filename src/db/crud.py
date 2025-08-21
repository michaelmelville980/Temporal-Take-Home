from sqlalchemy.orm import Session
from . import models

def create_event(db: Session, order_id: str, type: str, payload_json: dict = None):
    event = models.Events(order_id=order_id, type=type, payload_json=payload_json)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def create_order(db: Session, order_id: str):
    order = models.Orders(id=order_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    create_event(db, order.id, "order_received")
    return order