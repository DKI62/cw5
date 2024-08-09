import pytest
import requests
from unittest.mock import patch
from src.api import HHVacanciesAPI


@pytest.fixture
def api():
    return HHVacanciesAPI()


@patch('requests.get')
def test_get_employers(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "Test Employer"}

    employer_ids = ["123", "456"]
    result = api.get_employers(employer_ids)

    assert len(result) == 2
    assert result[0]["name"] == "Test Employer"


@patch('requests.get')
def test_get_employers_not_found(mock_get, api):
    mock_get.return_value.status_code = 404

    employer_ids = ["999"]
    result = api.get_employers(employer_ids)

    assert len(result) == 0


@patch('requests.get')
def test_get_vacancies(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"items": [{"name": "Test Vacancy"}]}

    employer_id = "123"
    result = api.get_vacancies(employer_id)

    assert len(result) == 1
    assert result[0]["name"] == "Test Vacancy"
