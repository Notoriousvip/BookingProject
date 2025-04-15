import allure
import pytest
import requests
from requests import HTTPError


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_successfully(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    with allure.step("Sending request to create a booking"):
        response = api_client.create_booking(booking_data)

    with allure.step("Checking that the response status code is 200 or 201"):
        assert response.status_code in [200, 201], f"Expected status 200 or 201 but got {response.status_code}"

    with allure.step("Checking that the booking data in the response matches the sent data"):
        response_json = response.json()
        booking = response_json["booking"]

        assert booking["firstname"] == booking_data[
            "firstname"], f"Expected firstname {booking_data['firstname']} but got {booking['firstname']}"
        assert booking["lastname"] == booking_data[
            "lastname"], f"Expected lastname {booking_data['lastname']} but got {booking['lastname']}"
        assert booking["totalprice"] == booking_data[
            "totalprice"], f"Expected totalprice {booking_data['totalprice']} but got {booking['totalprice']}"
        assert booking["depositpaid"] == booking_data[
            "depositpaid"], f"Expected depositpaid {booking_data['depositpaid']} but got {booking['depositpaid']}"
        assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"][
            "checkin"], f"Expected checkin date {booking_data['bookingdates']['checkin']} but got {booking['bookingdates']['checkin']}"
        assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"][
            "checkout"], f"Expected checkout date {booking_data['bookingdates']['checkout']} but got {booking['bookingdates']['checkout']}"
        assert booking["additionalneeds"] == booking_data[
            "additionalneeds"], f"Expected additionalneeds {booking_data['additionalneeds']} but got {booking['additionalneeds']}"


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with invalid data')
def test_create_booking_with_invalid_data(api_client):
    booking_data = {
        "firstname": "John"
    }

    with allure.step("Sending request to create a booking with invalid data"):
        with pytest.raises(HTTPError) as error_info:
            api_client.create_booking(booking_data)

    with allure.step("Checking that the server returned an appropriate error"):
        error_text = str(error_info.value)
        assert "400" in error_text or "500" in error_text, f"Expected 400 or 500 error, but got: {error_text}"
