from parsers.base_parser import BaseParser


class ThemeParser(BaseParser):
    """The main class for the ThemeParser."""

    def __init__(self, subparsers) -> None:
        super().__init__(subparsers, "theme", "Manage themes.")

        self.parser.add_argument(
            "-c", "--create", metavar="name", help="Create a new theme."
        ),
        self.parser.add_argument(
            "-d", "--delete", metavar="name", help="Delete a theme."
        )
        self.parser.add_argument("--wipe", action="store_true", help="Wipe all themes.")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all created themes."
        )
        self.parser.add_argument("-a", "--apply", metavar="name", help="Apply a theme.")
        self.parser.add_argument(
            "-r",
            "--reload",
            action="store_true",
            help="Run reload commands on known configs.",
        )
