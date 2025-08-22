from sqlalchemy.orm import Session
from . import models
from typing import Dict, Any, List
from decimal import Decimal

def create_event(db: Session, order_id: str, type: str, payload_json: dict):
    event = models.Events(order_id=order_id, type=type, payload_json=payload_json)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def create_order(db: Session, order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):
    
    # Return existing row if order already exists
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order:
        return order  
    
    # Else, adds new order to database 
    order = models.Orders(id=order_id, items=items, address_json=address_json)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def validate_order(db: Session, order_id: str):
    
    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Mark order as validated and update database
    order.state = "validated"
    db.commit()
    db.refresh(order)
    return order


def charge_payment(db: Session, order_id: str, payment_id: str):

    # Avoids double-charges and retries failed payments
    payment = db.query(models.Payments).filter_by(payment_id=payment_id).one_or_none()
    if payment:
        if payment.status == "failed":
            payment.status = "charged"
            db.commit()
            db.refresh(payment)
        return payment
    
    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Computes total cost and adds new payment to database 
    cost = Decimal("0.00")
    for item in order.items:
        cost += item["qty"] * Decimal(str(item["price"]))
    payment = models.Payments(
        payment_id=payment_id,
        order_id=order_id,
        status="charged",
        amount=cost
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def prepare_package(db: Session, order_id: str):

    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Mark package as prepared and update database
    order.state = "package_prepared"
    db.commit()
    db.refresh(order)
    return order


def dispatch_carrier(db: Session, order_id: str):

    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Dispatch carrier and update database
    order.state = "carrier_dispatched"
    db.commit()
    db.refresh(order)
    return order

def ship_order(db: Session, order_id: str):

    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Ship package and update database
    order.state = "shipped"
    db.commit()
    db.refresh(order)
    return order

def remove_and_refund_order(db: Session, order_id: str, payment_id: str):

    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Mark order as cancelled (retains record in DB)
    order.state = "cancelled"
    db.commit()
    db.refresh(order)

    # If payment was charged, updates status to refunded
    payment = db.query(models.Payments).filter_by(payment_id=payment_id).one_or_none()
    if payment and payment.status == "charged":
        payment.status = "refunded"
        db.commit()
        db.refresh(payment)

def change_address(db: Session, order_id: str, address: Dict[str, Any]):

    # Raise error if order doesn't exist
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        raise ValueError(f"Order {order_id} not found")
    
    # Updates address
    order.address_json = address
    db.commit()
    db.refresh(order)


       
