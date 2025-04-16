import allure
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        response_data = response.json()
        BookingResponse(**response_data)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response_data["booking"]["firstname"] == booking_data["firstname"]
    assert response_data["booking"]["lastname"] == booking_data["lastname"]
    assert response_data["booking"]["totalprice"] == booking_data["totalprice"]
    assert response_data["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response_data["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response_data["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert response_data["booking"]["additionalneeds"] == booking_data["additionalneeds"]


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking using date fixture')
def test_create_booking_with_generated_dates(api_client, booking_dates):
    booking_data = {
        "firstname": "Ryan",
        "lastname": "Gosling",
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": booking_dates,
        "additionalneeds": "Lunch"
    }

    response = api_client.create_booking(booking_data)
    response_data = response.json()

    try:
        BookingResponse(**response_data)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response_data["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response_data["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with required fields only')
def test_create_booking_with_required_fields_only(api_client, booking_dates):
    booking_data = {
        "firstname": "Kanye",
        "lastname": "West",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": booking_dates
    }
    # additionalneeds не указываем тк опциональный параметр
    response = api_client.create_booking(booking_data)
    response_data = response.json()

    try:
        BookingResponse(**response_data)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response_data["booking"]["firstname"] == booking_data["firstname"]
    assert response_data["booking"]["lastname"] == booking_data["lastname"]
    assert response_data["booking"]["totalprice"] == booking_data["totalprice"]
    assert response_data["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response_data["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response_data["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert response_data["booking"].get("additionalneeds") in (None, "")
