import os
import sys
import shutil
import subprocess
from pathlib import Path


import platformdirs


from core.errors import (
    DirectoryNameError,
    StashNotFoundError,
    NoEntrysError,
    StashExistsError,
)


class StashService:
    """The main service for stashing."""

    def __init__(self):
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "stasher"
        self.active_file = self.root_dir / "active.txt"
        self.stashes_dir = self.root_dir / "stashes"

    def _validate_name(self, name: str) -> None:
        """Validate a name to be used for a stash."""
        name = name.strip()
        if "/" in name:
            raise DirectoryNameError(
                f"name: '{name}' consists of forbidden character: '/'."
            )
        elif len(name) == 0:
            raise DirectoryNameError("name cannot be an empty.")

        for char in name:
            if char != ".":
                return

        raise DirectoryNameError("name cannot only consist of dots.")

    def _get_stash(self, name: str) -> Path:
        """Check if a stash exists and return it."""
        path = self.stashes_dir / name
        if not path.exists():
            raise StashNotFoundError(f"stash with name: '{name}' was not found.")
        else:
            return path

    def create(self, name: str) -> None:
        """Create a new stash."""
        self._validate_name(name)

        path = self.stashes_dir / name
        if os.path.exists(path):
            raise StashExistsError(f"stash with name: '{name}' already exists.")
        else:
            path.mkdir()

    def delete(self, name: str) -> None:
        """Delete a stash."""
        path = self._get_stash(name)

        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"Could not remove directory '{path}': {e}", file=sys.stderr)
            sys.exit(1)

    def list(self) -> None:
        """List all created stashes."""
        for stash in os.listdir(self.stashes_dir):
            path = os.path.join(self.stashes_dir, stash)
            if os.path.isdir(path):
                print(stash)

    def activate(self, name: str) -> None:
        """Activate a stash."""
        if not self._get_stash(name):
            return

        with open(self.active_file, "w") as f:
            f.write(name)
