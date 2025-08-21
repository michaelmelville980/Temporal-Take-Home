from db import crud, models

# Inputs
ORDER_ID = "abc"
ORDER_ID_2 = "abcd"
ORDER_ITEM = [{"name": "apple", "qty": 2, "price": 5.00}]
ORDER_ITEM_2 = [{"name": "app", "qty": 1, "price": 100.00}]
ORDER_ADDRESS = {"address": "575 Lake Dr.", "city": "Sylvania", "state": "OH", "zipcode": "43560"}
ORDER_ADDRESS_2 = {"address": "5 Lake Dr.", "city": "Temp", "state": "AL", "zipcode": "43561"}

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


def test_validate_order(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM, ORDER_ADDRESS)
    crud.validate_order(db_session, ORDER_ID)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "validated"
    assert got.items == ORDER_ITEM
    assert got.address_json == ORDER_ADDRESS











