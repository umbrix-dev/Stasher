import argparse
from typing import Callable


from core.parser import Parser


class Cli:
    def __init__(self, pathService, stashService) -> None:
        """Setup parser."""
        self.parser = Parser()

    def execute(self) -> None:
        """Execute the cli."""
        args = self.parser.parser.parse_args()
        print(args.command)
