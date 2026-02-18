from parsers.base_parser import BaseParser


class StashParser(BaseParser):
    """The main class for the StashParser."""

    def __init__(self, subparsers) -> None:
        super().__init__(subparsers, "stash", "Manage stashes.")

        self.parser.add_argument(
            "-c", "--create", metavar="name", help="Create a new stash."
        ),
        self.parser.add_argument(
            "-d", "--delete", metavar="name", help="Delete a stash."
        )
        self.parser.add_argument("--wipe", action="store_true", help="Wipe all stashes.")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all created stashes."
        )
        self.parser.add_argument("-a", "--apply", metavar="name", help="Apply a stash.")
        self.parser.add_argument(
            "-r",
            "--reload",
            action="store_true",
            help="Run reload commands on known configs.",
        )
