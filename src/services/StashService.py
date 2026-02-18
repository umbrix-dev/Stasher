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
    """The main class for the StashService."""

    def __init__(self, pathService):
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "stasher"
        self.stashes_dir = self.root_dir / "stashes"
        self.pathService = pathService

    def _validate_dir_name(self, name: str) -> None:
        """Validate a name to be used for a directory."""
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
        """Check if a stash exists and return it"""
        stash_path = self.stashes_dir / name
        if not os.path.exists(stash_path):
            raise StashNotFoundError(f"stash with name: '{name}' was not found.")
        else:
            return stash_path

    def create_stash(self, name: str) -> None:
        """Create a new stash with the given name."""
        self._validate_dir_name(name)

        data = self.pathService.load_paths_data()
        if len(data) < 1:
            raise NoEntrysError(
                "Make sure to add a path entry before creating a stash."
            )

        stash_path = self.stashes_dir / name
        if os.path.exists(stash_path):
            raise StashExistsError(f"stash with name: '{name}' already exists.")
        else:
            for path_key, path_entry in data.items():
                dest_path = stash_path / path_key
                try:
                    shutil.copytree(path_entry, dest_path)
                except Exception as e:
                    print(
                        f"Could not copy directory '{path_entry}' to '{path_key}': {e}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

    def delete_stash(self, name: str) -> None:
        """Delete a stash with the given name."""
        stash_path = self._get_stash(name)

        try:
            shutil.rmtree(stash_path)
        except Exception as e:
            print(f"Could not remove directory '{stash_path}': {e}", file=sys.stderr)
            sys.exit(1)

    def list_stashes(self) -> None:
        """List all created stashes."""
        for stash in os.listdir(self.stashes_dir):
            if os.path.isdir(os.path.join(self.stashes_dir, stash)):
                print(stash)

    def wipe_stashes(self) -> None:
        """Reset and remove all stashes."""
        for stash in os.listdir(self.stashes_dir):
            full_path = os.path.join(self.stashes_dir / stash)
            if os.path.isdir(full_path):
                try:
                    shutil.rmtree(full_path)
                except Exception as e:
                    print(
                        f"Could not remove directory '{full_path}': {e}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

    def apply_stash(self, name: str) -> None:
        """Apply a stash with the given name."""
        stash_path = self._get_stash(name)
        data = self.pathService.load_paths_data()
        for config_dir in os.listdir(stash_path):
            if config_dir in data:
                shutil.copytree(
                    stash_path, Path(data[config_dir]).parent, dirs_exist_ok=True
                )

    def reload_stashes(self) -> None:
        commands = [["hyprctl", "reload"], ["killall", "-SIGUSR2", "waybar"]]
        for cmd in commands:
            try:
                subprocess.run(cmd, check=False)
            except Exception:
                pass
