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


@allure.feature('Test Booking')
@allure.story('Test server unavailability during booking creation')
def test_create_booking_server_unavailable(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))

    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Booking')
@allure.story('Test booking creation with wrong HTTP method')
def test_create_booking_wrong_method(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 405"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Booking')
@allure.story('Test internal server error during booking creation')
def test_create_booking_internal_server_error(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 500"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Booking')
@allure.story('Test booking creation with wrong URL')
def test_create_booking_not_found(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 404"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Booking')
@allure.story('Test timeout during booking creation')
def test_create_booking_timeout(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, 'post', side_effect=Timeout)

    with pytest.raises(Timeout):
        api_client.create_booking(generate_random_booking_data)
