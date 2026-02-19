from typing import Callable


from core.parser import Parser


class Cli:
    def __init__(self, service) -> None:
        """Setup parser."""
        self.parser = Parser()
        self.service = service
        self.command_map = self._setup_command_map()

    def _setup_command_map(
        self,
    ) -> dict[str, dict[str, list[Callable, tuple[str, ...]]]]:
        """Setup and return the command map."""
        return {
            "create": [self.service.create, "name"],
            "delete": [self.service.delete, "name"],
            "list": [self.service.list],
            "activate": [self.service.activate, "name"],
            "clear": [self.service.clear],
            "status": [self.service.status],
            "tree": [self.service.tree, "name"],
            "track": [self.service.track, "path"],
            "tracked": [self.service.tracked],
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
