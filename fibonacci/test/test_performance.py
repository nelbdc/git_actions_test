import pytest
from ..dynamic import fibonacci_dynamic_more
from ..conftest import track_performance,time_tracker_func
from time import sleep

@pytest.mark.performance
@track_performance
def test_performance():
    sleep(3)
    fibonacci_dynamic_more(1000)