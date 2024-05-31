import os
import pytest

# Add any global fixtures or configuration here
os.environ['BACKEND_ENV'] = 'test'

# Example fixture
@pytest.fixture
def example_fixture():
  # Setup code for the fixture
  yield
  # Teardown code for the fixture

# Add any other fixtures or configuration specific to your project