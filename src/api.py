"""
api.py - Exposes a clean and stable API for frontends
"""

from core.stasher import Stasher


_stasher = Stasher()


def setup() -> None:
    """Setup Stasher."""
    _stasher.setup()
