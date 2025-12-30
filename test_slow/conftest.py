"""
Pytest configuration for slow integration tests.

This module configures pytest to properly discover and run slow integration tests.
"""

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line(
        "markers", "slow: mark test as slow (deselect with '-m \"not slow\"')"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark tests in test_slow as 'slow' and 'integration'.

    This allows users to easily skip slow tests with:
        pytest -m "not slow"
    """
    for item in items:
        # Mark all tests in test_slow as slow and integration
        if "test_slow" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.integration)
