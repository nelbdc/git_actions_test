from datetime import datetime, timedelta
import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f"\nruntime {diff.total_seconds()}")


class PerformaException(Exception):
    def __init__(self, runtime, timedelta):
        self.runtime = runtime
        self.limit = timedelta

    def __str__(self):
        return f"Performance test failed, runtime: {self.runtime.total_seconds()}, limit: {self.limit.total_seconds()}"


def track_performance(method, runtime_limit=timedelta(seconds=2)):
    def run_function_and_validate_runtime(*args, **kwargs):
        tick = datetime.now()
        resulst = method(*args, **kwargs)
        tock = datetime.now()
        runtime = tock - tick
        print(f"\nruntime {runtime.total_seconds()}")

        if runtime > runtime_limit:
            raise PerformaException(runtime, runtime_limit)
        return resulst

    return run_function_and_validate_runtime


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
