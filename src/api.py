"""
api.py - Exposes a clean and stable API for frontends
"""

from core.stasher import Stasher
from services.PathServiceOld import PathService


_stasher = Stasher()
_pathService = PathService()


def setup() -> None:
    """Setup Stasher."""
    _stasher.setup()


def add_path(path: str) -> None:
    """Add a new path."""
    _pathService.create_path(path)


def remove_path(path_or_key: str) -> None:
    """Remove a path."""
    _pathService.remove_path(path_or_key)


def get_paths() -> list[str] | None:
    """Get paths."""
    return _pathService.get_paths()
