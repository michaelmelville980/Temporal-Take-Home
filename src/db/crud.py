from sqlalchemy.orm import Session
from . import models
from typing import Dict, Any, List

def create_event(db: Session, order_id: str, type: str, payload_json: dict = None):
    event = models.Events(order_id=order_id, type=type, payload_json=payload_json)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def create_order(db: Session, order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):
    order = models.Orders(id=order_id, items=items, address_json=address_json)
    db.add(order)
    db.commit()
    db.refresh(order)
    create_event(db, order.id, "order_received", {"items": items, "address": address_json})
    return order

def validate_order(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order.items and len(order.items) > 0:
        order.state = "validated"
        db.commit()
        db.refresh(order)
        create_event(db, order.id, "order_validated", {"state": order.state})
    return order

def charge_payment(db: Session, order_id: str, payment_id: str):
    payment = db.query(models.Payments).filter_by(payment_id = payment_id).one_or_none()
    if payment:
        if payment.status == "failed":
            payment.status="charged"
            db.commit()
            db.refresh(payment)
        return payment
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    cost = 0.0
    for item in order.items:
        cost += item["qty"] * item["price"]
    payment = models.Payments(payment_id = payment_id, order_id=order_id, status="charged", amount=cost)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def prepare_package(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order.items and len(order.items) > 0:
        order.state = "package_prepared"
        db.commit()
        db.refresh(order)
        create_event(db, order.id, "package_prepared", {"state": order.state})
    return order

def dispatch_carrier(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order.items and len(order.items) > 0:
        order.state = "carrier_dispatched"
        db.commit()
        db.refresh(order)
        create_event(db, order.id, "carrier_dispatched", {"state": order.state})
    return order

def ship_order(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order.items and len(order.items) > 0:
        order.state = "shipped"
        db.commit()
        db.refresh(order)
        create_event(db, order.id, "shipped", {"state": order.state})
    return order

    

        
    






