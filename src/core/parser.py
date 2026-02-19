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
            "untrack": self._create_parser("untrack", "Untrack a path.", "path"),
            "tracked": self._create_parser(
                "tracked", "List all tracked paths in the current active stash."
            ),
            "auth": self._create_parser(
                "auth", "Create a safety layer to securely handle dangerous actions."
            ),
            "wipe": self._create_parser("wipe", "Wipe all stashes."),
            "status": self._create_parser("status", "Show current active stash."),
            "update": self._create_parser(
                "update", "Update current active stash with changed files."
            ),
            "merge": self._create_parser(
                "merge", "Merge 2 stashes together.", "name_1", "name_2"
            ),
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
