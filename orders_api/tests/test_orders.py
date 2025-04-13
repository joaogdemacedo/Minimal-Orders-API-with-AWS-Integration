import base64
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

FAKE_JWT = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTEyMyIsImV4cCI6MTc3NTc1NTQ0NX0.5N-UlFBveiBXc8tSQS7_4We2XCWt_SPepyWysSJ3zrs"
headers = {"Authorization": FAKE_JWT}

def test_create_order():
    response = client.post(
        "/orders/",
        json={
            "userId": "create-test-user",
            "items": [
                {"productId": "prod-1", "quantity": 2},
                {"productId": "prod-2", "quantity": 1}
            ]
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()

    assert "id" in data and isinstance(data["id"], str)
    assert data["userId"] == "create-test-user"
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 2
    for item in data["items"]:
        assert "productId" in item and isinstance(item["productId"], str)
        assert "quantity" in item and isinstance(item["quantity"], int)
    
def test_list_orders():
    # Create 2 test orders for reproducible pagination
    for i in range(2):
        client.post(
            "/orders/",
            json={
                "userId": "pagination-test-user",
                "items": [{"productId": f"item-{i}", "quantity": 1}]
            },
            headers=headers
        )

    response = client.get("/orders/?limit=1", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 1

    order = data["items"][0]
    assert "id" in order and isinstance(order["id"], str)
    assert "userId" in order and isinstance(order["userId"], str)
    assert "items" in order and isinstance(order["items"], list)

    # Validate inner structure of items
    for item in order["items"]:
        assert "productId" in item and isinstance(item["productId"], str)
        assert "quantity" in item and isinstance(item["quantity"], int)

    # Pagination check
    next_key = data.get("next_key")
    if next_key:
        next_response = client.get(f"/orders/?limit=1&start_key={next_key}", headers=headers)
        assert next_response.status_code == 200

        next_data = next_response.json()
        assert len(next_data["items"]) == 1
        assert next_data["items"][0]["id"] != order["id"]
    
def test_list_orders_with_invalid_limit():
    """
    Tests that limit=0 (invalid input) is rejected.
    """
    response = client.get("/orders/?limit=0", headers=headers)
    assert response.status_code in (400, 422)
    
def test_list_orders_with_large_limit():
    """
    Tests that the maximum allowed limit (100) works without crashing.
    """
    response = client.get("/orders/?limit=100", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 100    
    
def test_list_orders_exceeds_max_limit():
    """
    Tests that exceeding the max limit returns a 422 error.
    """
    response = client.get("/orders/?limit=1000", headers=headers)
    assert response.status_code == 422
    
def test_list_orders_with_invalid_start_key():
    """
    Tests that a malformed start_key (not base64) returns an error.
    """
    invalid_key = "this_is_not_base64!@#$"
    response = client.get(f"/orders/?limit=1&start_key={invalid_key}", headers=headers)

    # Expected: 400 Bad Request (or 422 if you let FastAPI handle it)
    assert response.status_code in (400, 422)
    
def test_get_order_by_id():
    # Create order
    response = client.post(
        "/orders/",
        json={
            "userId": "read-test-user",
            "items": [{"productId": "abc", "quantity": 1}]
        },
        headers=headers
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    # Fetch order by ID
    get_response = client.get(f"/orders/{order_id}", headers=headers)
    assert get_response.status_code == 200
    order = get_response.json()

    assert order["id"] == order_id
    assert order["userId"] == "read-test-user"
    assert len(order["items"]) == 1
    assert order["items"][0]["productId"] == "abc"
     
def test_cancel_order():
    # Create order
    response = client.post(
        "/orders/",
        json={
            "userId": "cancel-test-user",
            "items": [{"productId": "to-cancel", "quantity": 3}]
        },
        headers=headers
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    # Cancel order
    cancel_response = client.delete(f"/orders/{order_id}", headers=headers)
    assert cancel_response.status_code == 200
    assert cancel_response.json() == {"message": "Order cancelled"}

    # Confirm canceled status
    get_response = client.get(f"/orders/{order_id}", headers=headers)
    assert get_response.status_code == 200
    order = get_response.json()
    assert order["status"] == "cancelled"
    
def test_get_order_not_found():
    """
    Tests that fetching a non-existent order returns a 404 error.
    """
    response = client.get("/orders/this-id-does-not-exist", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
    
def test_cancel_order_not_found():
    """
    Tests that cancelling a non-existent order returns a 404 error.
    """
    response = client.delete("/orders/this-id-does-not-exist", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
    
def test_list_orders_with_dead_cursor():
    """
    Tests that a valid but non-existent start_key returns an empty result (not an error).
    """
    # Simulate a valid base64-encoded start_key for a non-existent order ID
    fake_key_dict = {"id": "dead-id-123"}
    encoded = base64.b64encode(json.dumps(fake_key_dict).encode("utf-8")).decode("utf-8")

    response = client.get(f"/orders/?limit=1&start_key={encoded}", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    # It's acceptable for it to be empty or contain only unrelated data, depending on ordering
    
def test_create_order_rejects_xss_userid():
    """
    Tests that userId with script tags is rejected (XSS prevention).
    """
    response = client.post(
        "/orders/",
        json={
            "userId": "<script>alert('x')</script>",
            "items": [{"productId": "prod-1", "quantity": 1}]
        },
        headers=headers
    )
    assert response.status_code == 422
    assert "userId" in response.text