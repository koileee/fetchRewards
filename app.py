from flask import Flask, request, jsonify
from calculate import calculate_points
import uuid
import re

app = Flask(__name__)

# In-memory dictionary to store receipts and their IDs
receipt_points = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    try:
        # Get the JSON receipt from the request
        receipt_json = request.get_json()

        # Generate a unique ID for the receipt
        receipt_id = str(uuid.uuid4())

        # Calculate points for the receipt
        points = calculate_points(receipt_json)

        # Store the receipt points with its generated ID
        receipt_points[receipt_id] = points

        # Prepare the response JSON
        response = {"id": receipt_id}

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to process receipt", "details": str(e)}), 500

@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    try:
        # Check if the receipt ID exists in the receipt_points dictionary
        if receipt_id in receipt_points:
            points = receipt_points[receipt_id]
            response = {"points": points}
            return jsonify(response), 200
        else:
            return jsonify({"error": "Receipt not found"}), 404

    except Exception as e:
        return jsonify({"error": "Failed to get points", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

