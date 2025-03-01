import pytest
from fastapi.testclient import TestClient


def test_get_odd_numbers_success(client: TestClient, api_v1_prefix: str):
    """Test getting odd numbers successfully."""
    response = client.get(f"{api_v1_prefix}/odd-numbers/?start=1&end=10")
    assert response.status_code == 200
    assert response.json() == {"odd_numbers": [1, 3, 5, 7, 9]}


def test_get_odd_numbers_invalid_range(client: TestClient, api_v1_prefix: str):
    """Test getting odd numbers with invalid range."""
    response = client.get(f"{api_v1_prefix}/odd-numbers/?start=10&end=1")
    assert response.status_code == 400
    assert "Start (10) must be less than or equal to end (1)" in response.json()["detail"]


def test_get_odd_numbers_sum_exceeds_limit(client: TestClient, api_v1_prefix: str):
    """Test getting odd numbers with sum exceeding limit."""
    response = client.get(f"{api_v1_prefix}/odd-numbers/?start=1&end=20")
    assert response.status_code == 400
    assert "Sum of odd numbers" in response.json()["detail"]


@pytest.mark.parametrize(
    "start,end,expected_numbers",
    [
        (1, 5, [1, 3, 5]),
        (0, 10, [1, 3, 5, 7, 9]),
        (5, 5, [5]),
    ],
)
def test_get_odd_numbers_parametrized(
    client: TestClient, api_v1_prefix: str, start: int, end: int, expected_numbers: list
):
    """Test getting odd numbers with different ranges."""
    response = client.get(f"{api_v1_prefix}/odd-numbers/?start={start}&end={end}")
    assert response.status_code == 200
    assert response.json() == {"odd_numbers": expected_numbers}


@pytest.mark.parametrize(
    "start,end",
    [
        (-1, 5),
        (5, -1),
        (100, 200),
    ],
)
def test_get_odd_numbers_invalid_input(
    client: TestClient, api_v1_prefix: str, start: int, end: int
):
    """Test getting odd numbers with invalid input."""
    response = client.get(f"{api_v1_prefix}/odd-numbers/?start={start}&end={end}")
    assert response.status_code == 400 