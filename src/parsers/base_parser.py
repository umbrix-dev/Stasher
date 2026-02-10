import argparse


class BaseParser:
    """The base class for all subparsers."""

    def __init__(
        self,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
        name: str = "",
        help: str = "",
    ) -> None:
        self.parser = subparsers.add_parser(name, help=help)

    def print_usage(self) -> None:
        self.parser.print_usage()
