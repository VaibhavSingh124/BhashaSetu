"""
pytest configuration and marker registration for BhashaSetu tests.
"""
import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: mark test as requiring real model/internet (deselect with -m 'not integration')",
    )
