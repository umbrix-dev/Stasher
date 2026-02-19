"""
Stasher - v1.3
https://github.com/umbrix-dev/Stasher
-----------------------------------------------
A Simple snapshot manager for Linux.
"""

from core.stasher import Stasher


def main() -> None:
    """The main entry point for Stasher."""
    stasher = Stasher()
    stasher.run()


if __name__ == "__main__":
    main()
