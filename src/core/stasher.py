from pathlib import Path


import platformdirs


from services.stash_service import StashService
from core.cli import Cli
from core.utils import safemake


class Stasher:
    """The main class for Stasher."""

    def __init__(self) -> None:
        """Define paths."""
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "stasher"
        self.stashes_dir = self.root_dir / "stashes"
        self.stashService = StashService()
        self.cli = Cli(self.stashService)

    def setup(self) -> None:
        """Create required directorys and files."""
        safemake(
            {self.user_data_dir: False, self.root_dir: False, self.stashes_dir: False}
        )

    def run(self) -> None:
        """Setup and execute Stasher."""
        self.setup()
        self.cli.execute()


def main() -> None:
    """The main entry point for Stasher."""
    stasher = Stasher()
    stasher.run()


if __name__ == "__main__":
    main()
