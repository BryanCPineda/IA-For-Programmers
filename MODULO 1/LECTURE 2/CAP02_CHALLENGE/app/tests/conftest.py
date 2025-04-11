"""
Configuration for pytest.
This module contains setup and fixtures for all tests.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
