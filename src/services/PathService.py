import os
import json
from pathlib import Path


import platformdirs


from core.errors import IsAFileError, PathExistsError


class PathService:
    """The main class for the PathService."""

    def __init__(self) -> None:
        """Define paths."""
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "stasher"
        self.paths_data = self.root_dir / "paths.json"

    def _validate_path(self, path: str) -> None:
        """Validate a path entry."""
        path_object = Path(path)
        if not os.path.exists(path_object):
            raise FileNotFoundError(f"path: '{path}' was not found.")
        elif os.path.isfile(path_object):
            raise IsAFileError(f"path: '{path}' must be a directory, not a file.")

    def load_paths_data(self) -> dict[str, str] | dict:
        """Load paths data or default to empty dictionary."""
        with open(self.paths_data, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def create_path(self, path: str) -> None:
        """Create a new path entry."""
        self._validate_path(path)

        data = self.load_paths_data()

        with open(self.paths_data, "w") as f:
            name = str.split(path, "/")[-1]
            if data.get(name):
                raise PathExistsError(f"path: '{path}' is already an entry.")

            data[name] = path
            json.dump(data, f, indent=4)

    def remove_path(self, path_or_key: str) -> None:
        """Remove a path entry."""
        if path_or_key.strip() == "*":
            remove_all = (
                input("Are you sure you want to remove all path entrys?: [y/N]: ")
                .strip()
                .lower()
            )
            if "y" in remove_all:
                with open(self.paths_data, "w"):
                    pass
                return

        if "/" in path_or_key:
            path = path_or_key
        else:
            with open(self.paths_data, "r") as f:
                try:
                    path = json.load(f)[path_or_key]
                except KeyError:
                    raise KeyError(f"key: '{path_or_key}' was not found.")

        self._validate_path(path)

        with open(self.paths_data, "r") as f:
            try:
                data: dict[str, str] = json.load(f)
                for path_key, path_entry in data.items():
                    if path_entry == path:
                        del data[path_key]

                        with open(self.paths_data, "w") as f:
                            json.dump(data, f, indent=4)

                        break
            except json.JSONDecodeError:
                pass

    def list_paths(self) -> None:
        """List all path entrys."""
        with open(self.paths_data, "r") as f:
            try:
                data: dict[str, str] = json.load(f)
                for path_key, path_entry in data.items():
                    print(path_key, path_entry)
            except json.JSONDecodeError:
                pass

    def wipe_paths(self) -> None:
        """Clean and remove all paths."""
        with open(self.paths_data, "w"):
            pass
