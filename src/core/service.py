import os
import sys
import json
import shutil
from pathlib import Path


import platformdirs
from rich.tree import Tree
from rich import print as rprint


from core.errors import (
    DirectoryNameError,
    StashNotFoundError,
    StashExistsError,
)


def no_active_stash() -> None:
    print("No current active stash.")
    print("Activate one by doing: stasher activate <name>")


class Service:
    """The main service for Stasher."""

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

    def _validate_path(self, path: str) -> None:
        """Validate a path entry."""
        path_object = Path(path)
        if not path_object.exists():
            raise FileNotFoundError(f"path: '{path}' was not found.")

    def _get_stash(self, name: str) -> Path:
        """Check if a stash exists and return it."""
        path = self.stashes_dir / name
        if not path.exists() or path.parent.name != "stashes":
            raise StashNotFoundError(f"stash with name: '{name}' was not found.")
        else:
            return path

    def _get_stash_data(self, name: str) -> dict:
        """Get the data of a stash."""
        path = self._get_stash(name)
        data = path / ".stash.json"
        if data.exists():
            with open(data, "r") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(
                f"'.stash.json' could not be found in path: '{path}'."
            )

    def _write_stash_data(self, name: str, data: dict):
        """Write to the data of a stash."""
        path = self._get_stash(name)
        with open(path / ".stash.json", "w") as f:
            json.dump(data, f, indent=4)

    def _get_stash_code(self, name: str) -> int:
        """Check if a stash exists and return an exit code."""
        path = self.stashes_dir / name
        if not path.exists() or path.parent.name != "stashes":
            return 1
        else:
            return 0

    def _get_active_name(self) -> str | None:
        """Get the current active stash if it exists."""
        with open(self.active_file, "r") as f:
            name = f.read().strip()
            if self._get_stash_code(name) == 0:
                return name

    def _get_active_path(self) -> Path | None:
        """Get the current active stash path if it exists."""
        name = self._get_active_name()
        if not name:
            return

        path = self.stashes_dir / name
        if path.exists():
            return path

    def create(self, name: str) -> None:
        """Create a new stash."""
        self._validate_name(name)

        path = self.stashes_dir / name
        data = path / ".stash.json"

        if os.path.exists(path):
            raise StashExistsError(f"stash with name: '{name}' already exists.")
        else:
            path.mkdir()
            with open(data, "w") as f:
                json.dump({"tracked": {}}, f, indent=4)

    def delete(self, name: str) -> None:
        """Delete a stash."""
        path = self._get_stash(name)

        try:
            shutil.rmtree(path)

            active_name = self._get_active_name()
            if active_name == name:
                self.clear()
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

    def clear(self) -> None:
        """Go out of the current active stash."""
        with open(self.active_file, "w"):
            pass

    def status(self) -> None:
        """Print the current active stash."""
        active_name = self._get_active_name()
        if not active_name:
            no_active_stash()
        else:
            print(active_name)

    def push(self) -> None:
        """Push changes to the current active stash."""
        active_path = self._get_active_path()
        active_name = self._get_active_name()
        if not active_name:
            no_active_stash()
            return

        data = self._get_stash_data(active_name)
        for path in data["tracked"].values():
            dest = active_path / Path(path).name
            if os.path.isfile(path):
                shutil.copy2(path, dest)
            else:
                shutil.copytree(path, dest)

    def tree(self, name: str) -> None:
        """Print the tree of a stash."""

        def _build(path: Path, tree: Tree) -> None:
            """Recursively build the tree of a path."""
            for child in sorted(path.iterdir()):
                if child.is_dir():
                    branch = tree.add(f"{child.name}/")
                    _build(child, branch)
                else:
                    tree.add(child.name)

        path = self._get_stash(name)
        treeObj = Tree(path.name)
        _build(path, treeObj)
        rprint(treeObj)

    def track(self, path: str) -> None:
        """Track a path to the current active stash."""
        active_name = self._get_active_name()
        if not active_name:
            no_active_stash()
            return

        self._validate_path(path)

        data = self._get_stash_data(active_name)
        if path in data["tracked"].values():
            print("path already tracked.")
        else:
            data["tracked"][Path(path).name] = path
            self._write_stash_data(active_name, data)

    def untrack(self, path_or_key: str) -> None:
        """Untrack a path of the current active stash."""
        active_name = self._get_active_name()
        if not active_name:
            no_active_stash()
            return

        data = self._get_stash_data(active_name)
        for filename, tracked_path in data["tracked"].items():
            if path_or_key == filename:
                key = filename
                path = data["tracked"][path_or_key]
                break
            elif path_or_key == tracked_path:
                key = filename
                path = tracked_path
                break
            else:
                key = None
                path = None

        if not path or not key:
            raise FileNotFoundError(f"path: '{path}' was not found.")

        if not path in data["tracked"].values():
            print("path is not tracked.")
        else:
            data["tracked"].pop(key, None)
            self._write_stash_data(active_name, data)

    def tracked(self) -> None:
        """List all tracked paths of the current active stash."""
        active_name = self._get_active_name()
        if not active_name:
            no_active_stash()
            return

        data = self._get_stash_data(active_name)
        for filename, path in data["tracked"].items():
            print(filename, path)
