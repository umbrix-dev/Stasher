from parsers.base_parser import BaseParser


class PathParser(BaseParser):
    """The main class for the PathParser."""

    def __init__(self, subparsers):
        super().__init__(subparsers, "path", "Manage paths.")

        self.parser.add_argument("-a", "--add", metavar="path", help="Add a new path.")
        self.parser.add_argument("-r", "--remove", metavar="path", help="Remove a path")
        self.parser.add_argument("--wipe", action="store_true", help="Wipe all paths.")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all added paths."
        )
