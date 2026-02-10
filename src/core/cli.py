import argparse

from parsers.path_parser import PathParser
from parsers.theme_parser import ThemeParser


class Cli:
    def __init__(self, pathService, themeService):
        """Create parsers and arguments."""
        self.parser = argparse.ArgumentParser(
            description="A unique config manager for hyprland."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.pathParser = PathParser(self.subparsers)
        self.themeParser = ThemeParser(self.subparsers)
        self.pathService = pathService
        self.themeService = themeService

    def execute(self) -> None:
        """Execute the cli."""
        args = self.parser.parse_args()
        if args.command == "path":
            if args.add:
                self.pathService.create_path(args.add)
            elif args.remove:
                self.pathService.remove_path(args.remove)
            elif args.wipe:
                self.pathService.wipe_paths()
            elif args.list:
                self.pathService.list_paths()
            else:
                self.pathParser.print_usage()
        elif args.command == "theme":
            if args.create:
                self.themeService.create_theme(args.create)
            elif args.delete:
                self.themeService.delete_theme(args.delete)
            elif args.wipe:
                self.themeService.wipe_themes()
            elif args.list:
                self.themeService.list_themes()
            elif args.apply:
                self.themeService.apply_theme(args.apply)
            elif args.reload:
                self.themeService.reload_themes()
            else:
                self.themeParser.print_usage()
