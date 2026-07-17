# tests/conftest.py

import pytest
from praktikum.burger import Burger


@pytest.fixture
def burger():
    """Фикстура, создающая новый экземпляр Burger перед каждым тестом."""
    return Burger()
