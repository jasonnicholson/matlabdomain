#!/bin/bash
# Quick reference for running slow integration tests

# Run all slow tests (add -m slow because default addopts skip slow)
# Artifacts are kept under test_slow/artifacts/<project>/ (repo + docs/source)
pytest test_slow/ -v -s -m slow

# Run only a specific project test (filter by repo name or URL substring)
pytest test_slow/test_integration.py -v -s -m slow -k "matnwb"

# Verify project data is loaded
pytest test_slow/test_integration.py::test_project_data_exists -v -s

# Run all tests EXCEPT slow tests (regular test run)
pytest tests/ -v

# Run all tests excluding slow ones
pytest -m "not slow" -v

# Run with coverage report
pytest test_slow/test_integration.py --cov=sphinxcontrib --cov-report=term-missing --cov-report=html -v -s -m slow

# Dry run (just collect tests, don't run them)
pytest test_slow/ --collect-only -m slow
