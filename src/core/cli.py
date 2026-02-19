import argparse
from typing import Callable


from core.parser import Parser


class Cli:
    def __init__(self, stash_service) -> None:
        """Setup parser."""
        self.parser = Parser()
        self.stash_service = stash_service
        self.command_map = self._setup_command_map()

    def _setup_command_map(
        self,
    ) -> dict[str, dict[str, list[Callable, tuple[str, ...]]]]:
        return {
            "create": [self.stash_service.create, "name"],
            "delete": [self.stash_service.delete, "name"],
            "list": [self.stash_service.list],
            "activate": [self.stash_service.activate, "name"],
            "status": [self.stash_service.status],
        }

    def execute(self) -> None:
        """Execute the cli."""
        args = self.parser.parser.parse_args()
        mapping = self.command_map.get(args.command)
        if not mapping:
            return

        callback = mapping[0]
        parameters = []
        for parameter in mapping[1:]:
            parameters.append(getattr(args, parameter))

        callback(*parameters)
