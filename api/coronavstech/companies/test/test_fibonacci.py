import pytest
from django.urls import reverse
from datetime import datetime, timedelta
import json

fibonacci_reverse = reverse("fibonacci")
pytestmark = pytest.mark.django_db


@pytest.fixture
def time_tracker_func():
    limit = timedelta(seconds=2)
    tick = datetime.now()
    yield
    tock = datetime.now()
    runtime = tock - tick
    print(f"\nruntime {runtime.total_seconds()}")

    if runtime > limit:
        raise PerformaException(runtime, limit)

@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (20, 6765),
    ],
)
def test_fibonacci_url_should_ok_tt(client, n, expected):
    resulst = client.post(path=fibonacci_reverse, data={"number": n})
    assert resulst.status_code == 200
    response = json.loads(resulst.content)
    assert response["status"] == "success"
    assert response["info"] == expected


@pytest.mark.parametrize(
    "n,expected",
    [
        ("0o", "The number should be a digit"),
        ("1y", "The number should be a digit"),
        ("y2", "The number should be a digit"),
        ("ll", "The number should be a digit"),
        (-10, "The number should be a digit"),
    ],
)
def test_fibonacci_url_should_failed_tt(time_tracker_func,client, n, expected):
    resulst = client.post(path=fibonacci_reverse, data={"number": n})
    assert resulst.status_code == 404
    response = json.loads(resulst.content)
    assert response["status"] == "failed"
    assert response["info"] == expected

