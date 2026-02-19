import os
import sys
import shutil
from pathlib import Path


import platformdirs
from rich.tree import Tree
from rich import print as rprint


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
        if not path.exists() or path.parent.name != "stashes":
            raise StashNotFoundError(f"stash with name: '{name}' was not found.")
        else:
            return path

    def _get_stash_code(self, name: str) -> int:
        """Check if a stash exists and return an exit code."""
        path = self.stashes_dir / name
        if not path.exists() or path.parent.name != "stashes":
            return 1
        else:
            return 0

    def _get_active(self) -> str:
        """Get the current active stash."""
        with open(self.active_file, "r") as f:
            name = f.read().strip()
            if self._get_stash_code(name) == 0:
                return name

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

            active_name = self._get_active()
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
        with open(self.active_file, "r") as f:
            name = f.read().strip()
            if self._get_stash_code(name) == 1:
                print("No current active stash.")
                print("Activate one by doing: stasher activate <name>")
            else:
                print(name)

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
