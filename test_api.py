from app import app
import pytest
import requests
import json

# Assuming your Flask app is running at this base URL
BASE_URL = 'http://localhost:5000'

@pytest.fixture
def client():
    return app.test_client()


SAMPLE_RECEIPT_INPUT_1 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"}
    ],
    "total": "9.00"
}

def test_calculate_points(client):
    # Send a POST request to the /receipts/process endpoint with the sample input data
    response = client.post(f'{BASE_URL}/receipts/process', json=SAMPLE_RECEIPT_INPUT_1)

    # Check if the request was successful (HTTP status code 200)
    assert response.status_code == 200

    # Get the response JSON
    response_data = json.loads(response.text)

    # Get the response id
    id = response_data['id']

    # Send a GET request to the /receipts/{id}/points endpoint with the sample receipt ID
    response = client.get(f'{BASE_URL}/receipts/{id}/points')
    response = json.loads(response.text)

    # Check if the points in the response match the expected value (109)
    assert response["points"] == 109

# Add more test cases as needed

if __name__ == '__main__':
    pytest.main()
