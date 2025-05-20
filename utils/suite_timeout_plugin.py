import pytest
import time
import os

DEFAULT_TIMEOUT = int(os.getenv("SUITE_TIMEOUT_SEC", 900))

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Fail the suite if it runs longer than the given number of seconds (from SUITE_TIMEOUT_SEC in .env)"
    )

def pytest_sessionstart(session):
    session.start_time = time.time()

def pytest_sessionfinish(session, exitstatus):
    timeout = session.config.getoption("--suite-timeout")
    elapsed = time.time() - session.start_time
    if elapsed > timeout:
        pytest.exit(f"Test suite exceeded timeout of {timeout} seconds (elapsed: {elapsed:.2f})", returncode=1)