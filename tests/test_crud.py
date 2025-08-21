from db import crud, models

# Inputs
ORDER_ID = "abc"
ORDER_ID_2 = "abcd"
ORDER_ITEM = [{"name": "apple", "qty": 1, "price": 5.00}]
ORDER_ITEM_2 = [{"name": "app", "qty": 5, "price": 100.00}]
ORDER_ITEM_3 = [{"name": "app", "qty": 5, "price": 100.00}, {"name": "apple", "qty": 1, "price": 5.00}]
ORDER_ADDRESS = {"address": "575 Lake Dr.", "city": "Sylvania", "state": "OH", "zipcode": "43560"}
ORDER_ADDRESS_2 = {"address": "5 Lake Dr.", "city": "Temp", "state": "AL", "zipcode": "43561"}
PAYMENT_ID = "123"

# Tests
def test_create_order_single(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "received"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS

def test_create_order_multiple(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.create_order(db_session, ORDER_ID_2, ORDER_ITEM_2, ORDER_ADDRESS_2)
    got1 = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    got2 = db_session.query(models.Orders).filter_by(id=ORDER_ID_2).one_or_none()
    assert got1.id == ORDER_ID and got2.id == ORDER_ID_2
    assert got1.items == ORDER_ITEM and got2.items == ORDER_ITEM_2
    assert got1.address_json == ORDER_ADDRESS and got2.address_json == ORDER_ADDRESS_2

def test_create_order_idempotent(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    got = db_session.query(models.Orders).all()
    assert len(got) == 1

def test_validate_order(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.validate_order(db_session, ORDER_ID)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "validated"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS

def test_charge_payment_oneitem_onequantity(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    got = db_session.query(models.Payments).filter_by(payment_id=PAYMENT_ID).one_or_none()
    assert got is not None
    assert got.payment_id == PAYMENT_ID
    assert got.status == "charged"
    assert got.amount == 5.00

def test_charge_payment_oneitem_multiplequantity(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM_2, ORDER_ADDRESS)
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    got = db_session.query(models.Payments).filter_by(payment_id=PAYMENT_ID).one_or_none()
    assert got is not None
    assert got.payment_id == PAYMENT_ID
    assert got.status == "charged"
    assert got.amount == 500.00

def test_charge_payment_multipleitem_multiplequantity(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM_3, ORDER_ADDRESS)
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    got = db_session.query(models.Payments).filter_by(payment_id=PAYMENT_ID).one_or_none()
    assert got is not None
    assert got.payment_id == PAYMENT_ID
    assert got.status == "charged"
    assert got.amount == 505.00

def test_charge_payment_oneitem_onequantity_alreadypaid(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    got = db_session.query(models.Payments).all()
    assert len(got) == 1
    assert got[0].status == "charged"

def test_charge_payment_oneitem_onequantity_failedtopaid(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    failed = models.Payments(payment_id=PAYMENT_ID, order_id=ORDER_ID, status="failed", amount=5.00)
    db_session.add(failed)
    db_session.commit()
    crud.charge_payment(db_session, ORDER_ID, PAYMENT_ID)
    got = db_session.query(models.Payments).all()
    assert len(got) == 1
    assert got[0].status == "charged"

def test_prepare_package(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.prepare_package(db_session, ORDER_ID)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "package_prepared"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS


def test_dispatch_carrier(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.dispatch_carrier(db_session, ORDER_ID)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "carrier_dispatched"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS

def test_ship_order(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.ship_order(db_session, ORDER_ID)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "shipped"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS

def test_remove_and_refund_order_nopayment(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.remove_and_refund_order(db_session, ORDER_ID, PAYMENT_ID)
    gotOrder = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    gotPayment = db_session.query(models.Payments).filter_by(payment_id=PAYMENT_ID).one_or_none()
    assert gotOrder is not None
    assert gotOrder.id == ORDER_ID
    assert gotOrder.state == "cancelled"
    assert gotOrder.items == ORDER_ITEM
    assert gotOrder.address_json == ORDER_ADDRESS

def test_remove_and_refund_order_alreadypayed(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    payed = models.Payments(payment_id=PAYMENT_ID, order_id=ORDER_ID, status="charged", amount=5.00)
    db_session.add(payed)
    db_session.commit()
    crud.remove_and_refund_order(db_session, ORDER_ID, PAYMENT_ID)
    gotOrder = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    gotPayment = db_session.query(models.Payments).filter_by(payment_id=PAYMENT_ID).one_or_none()
    assert gotOrder is not None
    assert gotOrder.id == ORDER_ID
    assert gotOrder.state == "cancelled"
    assert gotOrder.items == ORDER_ITEM
    assert gotOrder.address_json == ORDER_ADDRESS
    assert gotPayment is not None
    assert gotPayment.payment_id == PAYMENT_ID
    assert gotPayment.status == "refunded"
    assert gotPayment.amount == 5.00










