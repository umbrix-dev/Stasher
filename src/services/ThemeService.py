import os
import sys
import shutil
import subprocess
from pathlib import Path

import platformdirs

from core.errors import (
    DirectoryNameError,
    ThemeNotFoundError,
    NoEntrysError,
    ThemeExistsError,
)


class ThemeService:
    """The main class for the ThemeService."""

    def __init__(self, pathService):
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "themeSwitcher"
        self.themes_dir = self.root_dir / "themes"

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

    def _get_theme(self, name: str) -> Path:
        """Check if a theme exists and return it"""
        theme_path = self.themes_dir / name
        if not os.path.exists(theme_path):
            raise ThemeNotFoundError(f"theme with name: '{name}' was not found.")
        else:
            return theme_path

    def create_theme(self, name: str) -> None:
        """Create a new theme with the given name."""
        self._validate_dir_name(name)

        data = self.pathService.load_paths_data()
        if len(data) < 1:
            raise NoEntrysError(
                "Make sure to add a path entry before creating a theme."
            )

        theme_path = self.themes_dir / name
        if os.path.exists(theme_path):
            raise ThemeExistsError(f"theme with name: '{name}' already exists.")
        else:
            for path_key, path_entry in data.items():
                dest_path = theme_path / path_key
                try:
                    shutil.copytree(path_entry, dest_path)
                except Exception as e:
                    print(
                        f"Could not copy directory '{path_entry}' to '{path_key}': {e}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

    def delete_theme(self, name: str) -> None:
        """Delete a theme with the given name."""
        theme_path = self._get_theme(name)

        try:
            shutil.rmtree(theme_path)
        except Exception as e:
            print(f"Could not remove directory '{theme_path}': {e}", file=sys.stderr)
            sys.exit(1)

    def list_themes(self) -> None:
        """List all created themes."""
        for theme in os.listdir(self.themes_dir):
            if os.path.isdir(os.path.join(self.themes_dir, theme)):
                print(theme)

    def wipe_themes(self) -> None:
        """Reset and remove all themes."""
        for theme in os.listdir(self.themes_dir):
            full_path = os.path.join(self.themes_dir / theme)
            if os.path.isdir(full_path):
                try:
                    shutil.rmtree(full_path)
                except Exception as e:
                    print(
                        f"Could not remove directory '{full_path}': {e}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

    def apply_theme(self, name: str) -> None:
        """Apply a theme with the given name."""
        theme_path = self._get_theme(name)
        data = self.pathService.load_paths_data()
        for config_dir in os.listdir(theme_path):
            if config_dir in data:
                shutil.copytree(
                    theme_path, Path(data[config_dir]).parent, dirs_exist_ok=True
                )

    def reload_themes(self) -> None:
        commands = [["hyprctl", "reload"], ["killall", "-SIGUSR2", "waybar"]]
        for cmd in commands:
            subprocess.run(cmd, check=False)
