from setuptools import setup, find_packages

setup(
    name="pytest_suite_timeout",
    version="0.1",
    description="Suite timeout plugin for pytest",
    packages=find_packages(),
    entry_points={"pytest11": ["suite_timeout = utils.suite_timeout_plugin"]},
    classifiers=["Framework :: Pytest"],
)