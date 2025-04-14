import allure
import pytest
import requests
from requests import Timeout


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_successfully(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"booking": {"id": 1, "name": "Test Booking"}}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    booking_data = {"name": "Test Booking", "date": "2025-04-20"}
    response = api_client.create_booking(booking_data)

    with allure.step("Asserting booking creation status code"):
        assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

    with allure.step("Asserting booking data is correct"):
        assert response["firstname"] == booking_data[
            "firstname"], f"Expected firstname {booking_data['firstname']} but got {response['firstname']}"
        assert response["lastname"] == booking_data[
            "lastname"], f"Expected lastname {booking_data['lastname']} but got {response['lastname']}"
        assert response["totalprice"] == booking_data[
            "totalprice"], f"Expected totalprice {booking_data['totalprice']} but got {response['totalprice']}"
        assert response["depositpaid"] == booking_data[
            "depositpaid"], f"Expected depositpaid {booking_data['depositpaid']} but got {response['depositpaid']}"
        assert response["bookingdates"]["checkin"] == booking_data["bookingdates"][
            "checkin"], f"Expected checkin date {booking_data['bookingdates']['checkin']} but got {response['bookingdates']['checkin']}"
        assert response["bookingdates"]["checkout"] == booking_data["bookingdates"][
            "checkout"], f"Expected checkout date {booking_data['bookingdates']['checkout']} but got {response['bookingdates']['checkout']}"


@allure.feature('Test Create Booking')
@allure.story('Test server unavailability during booking creation')
def test_create_booking_server_unavailable(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))

    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with invalid data')
def test_create_booking_with_invalid_data(api_client, mocker):
    booking_data = {
        "firstname": "John"
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    response = api_client.create_booking(booking_data)

    with allure.step("Checking that server returns error due to invalid data"):
        assert response.status_code == 400, f"Expected status 400 but got {response.status_code}"
