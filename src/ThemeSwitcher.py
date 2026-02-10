#!/bin/env python3

"""
ThemeSwitcher - v0.0.1
https://www.github.com/umbrix-dev/themeSwitcher
---------------------------------------------
Switch between themes using a simple cli tool
on hyprland.
"""


import os
import json
import shutil
import argparse
import platformdirs
from pathlib import Path


class IsAFileError(Exception):
    """Raised when a path is a file."""

    pass


class PathExistsError(Exception):
    """Raised when a path entry already exists."""

    pass


class DirectoryNameError(Exception):
    """Raised when a directory uses forbidden naming."""

    pass


class DirectoryExistsError(Exception):
    """Raised when a directory already exists."""

    pass


class NoEntrysError(Exception):
    """Raised when no path entries exist."""

    pass


class ThemeSwitcher:
    """The main class for ThemeSwitcher"""

    def __init__(self) -> None:
        """Define paths."""
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "themeSwitcher"
        self.themes_dir = self.root_dir / "themes"
        self.backups_dir = self.root_dir / "backups"
        self.auto_backups_dir = self.backups_dir / "auto"
        self.paths_data = self.root_dir / "paths.json"

    def _validate_path(self, path: str) -> None:
        """Validate a path entry."""
        path_object = Path(path)
        if not os.path.exists(path_object):
            raise FileNotFoundError(f"path: '{path}' was not found.")
        elif os.path.isfile(path_object):
            raise IsAFileError(f"path: '{path}' must be a directory, not a file.")

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

    def _create_path(self, path: str) -> None:
        """Create a new path entry."""
        self._validate_path(path)

        with open(self.paths_data, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        with open(self.paths_data, "w") as f:
            name = str.split(path, "/")[-1]
            if data.get(name):
                raise PathExistsError(f"path: '{path}' is already an entry.")

            data[name] = path
            json.dump(data, f, indent=4)

    def _remove_path(self, path_or_key: str) -> None:
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

    def _list_paths(self) -> None:
        """List all path entrys."""
        with open(self.paths_data, "r") as f:
            try:
                data: dict[str, str] = json.load(f)
                for path_key, path_entry in data.items():
                    print(path_key, path_entry)
            except json.JSONDecodeError:
                pass

    def _clean_paths(self) -> None:
        """Clean and remove all paths."""
        with open(self.paths_data, "w"):
            pass

    def _create_theme(self, name: str) -> None:
        """Create a new theme with the given name."""
        self._validate_dir_name(name)

        with open(self.paths_data, "r") as f:
            data = json.load(f)

        if len(data) < 1:
            raise NoEntrysError(
                "Make sure to add a path entry before creating a theme."
            )

        theme_path = self.themes_dir / name
        if os.path.exists(theme_path):
            raise DirectoryExistsError(f"theme with name: {name} already exists.")
        else:
            theme_path.mkdir()

    def _safemake(self, paths: dict[Path, bool]) -> None:
        """Safely create files/directorys if they dont exist"""
        for path, isFile in paths.items():
            if isFile:
                try:
                    path.touch()
                except FileExistsError:
                    pass
            else:
                try:
                    path.mkdir()
                except FileExistsError:
                    pass

    def _setup(self) -> None:
        """Create required directorys and files."""
        self._safemake(
            {
                self.user_data_dir: False,
                self.root_dir: False,
                self.themes_dir: False,
                self.backups_dir: False,
                self.auto_backups_dir: False,
                self.paths_data: True,
            }
        )

    def _create_path_parser(self) -> argparse.ArgumentParser:
        """Create and return the path parser."""
        path_parser = self.subparsers.add_parser("path", help="Manage paths.")
        path_parser.add_argument("-a", "--add", metavar="path", help="Add a new path.")
        path_parser.add_argument("-r", "--remove", metavar="path", help="Remove a path")
        path_parser.add_argument(
            "--clean", action="store_true", help="Clean and remove all paths."
        )
        path_parser.add_argument(
            "-l", "--list", action="store_true", help="List all added paths."
        )
        return path_parser

    def _create_theme_parser(self) -> argparse.ArgumentParser:
        """Create and return the theme parser."""
        theme_parser = self.subparsers.add_parser("theme", help="Manage themes.")
        theme_parser.add_argument(
            "-c", "--create", metavar="name", help="Create a new theme."
        )
        return theme_parser

    def _setup_cli(self) -> None:
        """Create parsers and arguments."""
        self.parser = argparse.ArgumentParser(
            description="A unique config manager for hyprland."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.path_parser = self._create_path_parser()
        self.theme_parser = self._create_theme_parser()

    def _handle_cli(self) -> None:
        """Handle commands and arguments."""
        args = self.parser.parse_args()
        if args.command == "path":
            if args.add:
                self._create_path(args.add)
            elif args.remove:
                self._remove_path(args.remove)
            elif args.list:
                self._list_paths()
            elif args.clean:
                self._clean_paths()
            else:
                self.path_parser.print_usage()
        elif args.command == "theme":
            if args.create:
                self._create_theme(args.create)
            else:
                self.theme_parser.print_usage()

    def run(self) -> None:
        """Setup and execute ThemeSwitcher."""
        self._setup()
        self._setup_cli()
        self._handle_cli()


def main() -> None:
    """The main entry point for ThemeSwitcher"""
    themeSwitcher = ThemeSwitcher()
    themeSwitcher.run()


if __name__ == "__main__":
    main()
