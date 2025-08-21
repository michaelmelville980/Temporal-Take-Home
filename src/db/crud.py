from sqlalchemy.orm import Session
from . import models
from typing import Dict, Any, List
from decimal import Decimal

def create_event(db: Session, order_id: str, type: str, payload_json: dict = None):
    event = models.Events(order_id=order_id, type=type, payload_json=payload_json)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def create_order(db: Session, order_id: str, items: List[Dict[str, Any]], address_json: Dict[str, Any]):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order:
        create_event(db, order_id, "create_order", {"message": "repeat request"})
        return order  
    order = models.Orders(id=order_id, items=items, address_json=address_json)
    db.add(order)
    db.commit()
    db.refresh(order)
    create_event(db, order_id, "create_order", {"message": "first request"})
    return order

def validate_order(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order is None:
        create_event(db, order_id, "validate_order", {"message": "error, no order found"})
    else:
        order.state = "validated"
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "validate_order", {"message": "success"})
    return order

def charge_payment(db: Session, order_id: str, payment_id: str):
    payment = db.query(models.Payments).filter_by(payment_id = payment_id).one_or_none()
    if payment:
        if payment.status == "failed":
            payment.status="charged"
            db.commit()
            db.refresh(payment)
            create_event(db, order_id, "charge_payment", {"message": "success, payment status changed from failed to charged"})
        if payment.status =="charged":
             create_event(db, order_id, "charge_payment", {"message": "customer already charged"})
        return payment
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if not order:
        create_event(db, order_id, "charge_payment", {"message": "error, no order found"})
        raise ValueError(f"Order {order_id} not found")
    cost = Decimal("0.00")
    for item in order.items:
        cost += item["qty"] * Decimal(str(item["price"]))
    payment = models.Payments(payment_id = payment_id, order_id=order_id, status="charged", amount=cost)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    create_event(db, order_id, "charge_payment", {"message": "first payment successful"})
    return payment

def prepare_package(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order is None:
        create_event(db, order_id, "prepare_package", {"message": "error, no order found"})
    if order.items and len(order.items) > 0:
        order.state = "package_prepared"
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "prepare_package", {"message": "success, package prepared"})
    return order

def dispatch_carrier(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order is None:
        create_event(db, order_id, "dispatch_carrier", {"message": "error, no order found"})
    if order.items and len(order.items) > 0:
        order.state = "carrier_dispatched"
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "dispatch_carrier", {"message": "success, carrier dispatched"})
    return order

def ship_order(db: Session, order_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()
    if order is None:
        create_event(db, order_id, "ship_order", {"message": "error, no order found"})
    if order.items and len(order.items) > 0:
        order.state = "shipped"
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "ship_order", {"message": "success, order shipped"})
    return order

def remove_and_refund_order(db: Session, order_id: str, payment_id: str):
    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()

    if order is None:
        create_event(db, order_id, "remove_and_refund_order", {"message": "error, no order found"})

    if order.items and len(order.items) > 0:

        # Cancelling Order
        order.state = "cancelled"
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "remove_and_refund_order", {"message": "success, order cancelled"})

        # Refunding Customer (if needed)
        payment = db.query(models.Payments).filter_by(payment_id=payment_id).one_or_none()
        if payment and payment.status == "charged":
            payment.status = "refunded"
            db.commit()
            db.refresh(payment)
            create_event(db, order_id, "remove_and_refund_order", {"message": "success, refund issued"})



def change_address(db: Session, order_id: str, address: Dict[str, Any]):

    order = db.query(models.Orders).filter_by(id=order_id).one_or_none()

    if order is None:
        create_event(db, order_id, "change_address", {"message": "error, no order found"})

    if order.items and len(order.items) > 0:
        order.address_json = address
        db.commit()
        db.refresh(order)
        create_event(db, order_id, "change_address", {"message": "success, address updated"})


    

        
    






