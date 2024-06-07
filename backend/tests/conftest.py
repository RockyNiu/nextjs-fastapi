import os

# Add any global fixtures or configuration here
os.environ["BACKEND_ENV"] = "test"

pytest_plugins = [
    "tests.utils.fixtures.item_conftest",
]
