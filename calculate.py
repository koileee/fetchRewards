import math
import re
from datetime import datetime

def calculate_points(receipt_json):
    # Rule 1: One point for every alphanumeric character in the retailer name.
    retailer_name = receipt_json.get("retailer", "")
    alphanumeric_count = len(re.sub(r'[^a-zA-Z0-9]', '', retailer_name))

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    total_amount = float(receipt_json.get("total", "0").replace("$", ""))
    is_round_dollar_amount = total_amount.is_integer()

    # Rule 3: 25 points if the total is a multiple of 0.25.
    is_multiple_of_025 = (total_amount * 100) % 25 == 0

    # Rule 4: 5 points for every two items on the receipt.
    items = receipt_json.get("items", [])
    item_count = len(items)
    item_points = item_count // 2 * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    item_description_points = sum(math.ceil(float(item.get("price", "0").replace("$", "")) * 0.2)
                                   for item in items if len(item.get("shortDescription", "")) % 3 == 0)

    # Rule 6: 6 points if the day in the purchase date is odd.
    purchase_date = receipt_json.get("purchaseDate", "")
    purchase_date_obj = datetime.strptime(purchase_date, "%Y-%m-%d")
    day_is_odd = purchase_date_obj.day % 2 != 0

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = receipt_json.get("purchaseTime", "")
    purchase_time_obj = datetime.strptime(purchase_time, "%H:%M")
    time_is_between_2_to_4 = purchase_time_obj.time() >= datetime.strptime("14:00", "%H:%M").time() and \
                              purchase_time_obj.time() < datetime.strptime("16:00", "%H:%M").time()

    # Calculate the total points based on the rules
    total_points = (
        alphanumeric_count +
        (50 if is_round_dollar_amount else 0) +
        (25 if is_multiple_of_025 else 0) +
        item_points +
        item_description_points +
        (6 if day_is_odd else 0) +
        (10 if time_is_between_2_to_4 else 0)
    )

    return total_points