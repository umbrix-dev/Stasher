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
        
    def create(self, name: str) -> None:
        """Create a new stash."""
        self._validate_name(name)
        
        path = self.stashes_dir / name
        if os.path.exists(path):
            raise StashExistsError(f"stash with name: '{name}' already exists.")
        else:
            path.mkdir()
            

    