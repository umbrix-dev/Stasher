import argparse
from typing import Callable


from parsers.path_parser import PathParser
from parsers.stash_parser import StashParser


class Cli:
    def __init__(self, pathService, stashService) -> None:
        """Create parsers and arguments."""
        self.parser = argparse.ArgumentParser(
            description="A simple snapshot manager for Linux."
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.pathParser = PathParser(self.subparsers)
        self.stashParser = StashParser(self.subparsers)
        self.pathService = pathService
        self.stashService = stashService
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
            "stash": {
                "create": [self.stashService.create_stash, ("create",)],
                "delete": [self.stashService.delete_stash, ("delete",)],
                "wipe": [self.stashService.wipe_stashes, ()],
                "list": [self.stashService.list_stashes, ()],
                "apply": [self.stashService.apply_stash, ("apply",)],
                "reload": [self.stashService.reload_stashes, ()],
                "_": [self.stashParser.print_usage, ()],
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

