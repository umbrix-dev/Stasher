import argparse
from typing import Any, Callable

from parsers.path_parser import PathParser
from parsers.theme_parser import ThemeParser


class Cli:
    def __init__(self, pathService, themeService) -> None:
        """Create parsers and arguments."""
        self.parser = argparse.ArgumentParser(
            description="A unique config manager for hyprland."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.pathParser = PathParser(self.subparsers)
        self.themeParser = ThemeParser(self.subparsers)
        self.pathService = pathService
        self.themeService = themeService
        self.command_map = self._setup_command_map()

    def _setup_command_map(
        self,
    ) -> dict[str, dict[str, list[Callable, tuple[str, ...]]]]:
        return {
            "path": {
                "add": [self.pathService.create_path, ("add",)],
                "remove": [self.pathService.remove_path, ("remove",)],
                "wipe": [self.pathService.wipe_paths, ()],
                "list": [self.pathService.list_paths, ()],
                "_": [self.pathParser.print_usage, ()],
            },
            "theme": {
                "create": [self.themeService.create_theme, ("create",)],
                "delete": [self.themeService.delete_theme, ("delete",)],
                "wipe": [self.themeService.wipe_themes, ()],
                "list": [self.themeService.list_themes, ()],
                "apply": [self.themeService.apply_theme, ("apply",)],
                "reload": [self.themeService.reload_themes, ()],
                "_": [self.themeParser.print_usage, ()],
            },
        }

    def execute(self) -> None:
        """Execute the cli."""
        args = self.parser.parse_args()
        group = self.command_map.get(args.command)
        if not group:
            return

        for command in group:
            try:
                if not getattr(args, command):
                    continue
            except AttributeError:
                callback = group[command][0]
                callback()
                return

            callback = group[command][0]
            callback_args = []
            for callback_arg in group[command][1]:
                try:
                    callback_args.append(getattr(args, callback_arg))
                except AttributeError:
                    pass

            callback(*callback_args)
            return
