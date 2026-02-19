import argparse


class Parser:
    """The main argument parsing handler for Stasher."""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="A simple snapshot manager for Linux."
        )
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.parsers = self._create_parsers()

    def _create_parsers(self) -> dict[str, argparse.ArgumentParser]:
        return {
            "create": self._create_parser("create", "Create a new stash.", "name"),
            "delete": self._create_parser("delete", "Delete a stash.", "name"),
            "list": self._create_parser("list", "List all created stashes."),
            "activate": self._create_parser("activate", "Activate a stash.", "name"),
            "clear": self._create_parser(
                "clear", "Go out of the current active stash."
            ),
            "track": self._create_parser("track", "Track a path.", "path"),
            "untrack": self._create_parser("untrack", "Untrack a path.", "path_or_key"),
            "tracked": self._create_parser(
                "tracked", "List all tracked paths in the current active stash."
            ),
            "status": self._create_parser("status", "Show current active stash."),
            "tree": self._create_parser("tree", "Print the tree of a stash.", "name"),
        }

    def _create_parser(
        self, name: str, help: str, *arguments: tuple[str]
    ) -> argparse.ArgumentParser:
        parser = self.subparsers.add_parser(
            name=name,
            help=help,
        )
        for argument in arguments:
            parser.add_argument(argument)
        return parser
