"""
Core module initialization.
This module contains core functionality and configuration for the NovelSpec backend.
"""

from typing import Dict, Any

# Version information
__version__ = "1.0.0"
__author__ = "NovelSpec Team"

# Core configuration
CONFIG: Dict[str, Any] = {
    "app_name": "NovelSpec",
    "debug": False,
    "api_version": "v1",
    "default_page_size": 20,
    "max_page_size": 100,
}

# Initialize core components
def init_core() -> None:
    """
    Initialize core components and configurations.
    Should be called when the application starts.
    """
    # This function can be expanded to include additional initialization logic
    pass

# Export commonly used components and utilities
from .config import settings  # type: ignore
from .security import get_password_hash, verify_password  # type: ignore
from .database import get_db  # type: ignore

__all__ = [
    "CONFIG",
    "init_core",
    "settings",
    "get_password_hash",
    "verify_password",
    "get_db",
]