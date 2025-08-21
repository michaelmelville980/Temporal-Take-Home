from db import crud, models

# Inputs
ORDER_ID = "abc"
ORDER_ID_2 = "abcd"
ORDER_ITEM = [{"name": "apple", "qty": 2, "price": 5.00}]
ORDER_ITEM_2 = [{"name": "app", "qty": 1, "price": 100.00}]

# Tests
def test_create_order_single(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM)
    got = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    assert got is not None
    assert got.id == ORDER_ID
    assert got.state == "received"
    assert got.items == ORDER_ITEM

def test_create_order_multiple(db_session):
    crud.create_order(db_session, ORDER_ID, ORDER_ITEM)
    crud.create_order(db_session, ORDER_ID_2, ORDER_ITEM_2)
    got1 = db_session.query(models.Orders).filter_by(id=ORDER_ID).one_or_none()
    got2 = db_session.query(models.Orders).filter_by(id=ORDER_ID_2).one_or_none()
    assert got1.id == ORDER_ID and got2.id == ORDER_ID_2
    assert got1.items == ORDER_ITEM and got2.items == ORDER_ITEM_2








